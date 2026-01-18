"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/agent/run.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../constants、../../GenericFunctions、../../transport。导出:description。关键函数/方法:execute、throwOperationErrorIf、extractAgentId、getAgentStatus、pollAgentStatus、Boolean。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/agent/run.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/agent/run_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INode,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';
import { jsonParse, NodeOperationError } from 'n8n-workflow';

import { AGENT_MIN_TIMEOUT_SECONDS, ERROR_MESSAGES } from '../../constants';
import { validateRequiredStringField } from '../../GenericFunctions';
import { apiRequest } from '../../transport';

const displayOptions = {
	show: {
		resource: ['agent'],
		operation: ['run'],
	},
};

export const description: INodeProperties[] = [
	{
		displayName: 'Webhook URL',
		name: 'webhookUrl',
		type: 'string',
		required: true,
		default: '',
		description:
			'Webhook URL to invoke the Airtop agent. Visit <a href="https://portal.airtop.ai/agents" target="_blank">Airtop Agents</a> for more information.',
		displayOptions,
	},
	{
		displayName: 'Parameters',
		name: 'agentParameters',
		type: 'json',
		required: true,
		default: '{}',
		description:
			'Agent\'s input parameters in JSON format. Visit <a href="https://portal.airtop.ai/agents" target="_blank">Airtop Agents</a> for more information.',
		displayOptions,
	},
	{
		displayName: 'Await Agent',
		name: 'awaitExecution',
		type: 'boolean',
		default: true,
		description: 'Whether to wait for the agent to complete its execution',
		displayOptions,
	},
	{
		displayName: 'Timeout',
		name: 'timeout',
		type: 'number',
		default: 600,
		description: 'Timeout in seconds to wait for the agent to finish',
		displayOptions: {
			show: {
				resource: ['agent'],
				operation: ['run'],
				awaitExecution: [true],
			},
		},
	},
];

interface AgentInvocationResponse extends IDataObject {
	invocationId: string;
}

interface AgentResultResponse extends IDataObject {
	status: 'Completed' | 'Running' | 'Failed' | 'Unknown';
	output?: IDataObject;
	error?: string;
}

function throwOperationErrorIf(statement: boolean, message: string, node: INode) {
	if (statement) {
		throw new NodeOperationError(node, message);
	}
}

/**
 * Extracts the agent ID from the webhook URL
 * Format: https://api.airtop.ai/api/hooks/agents/<agentId>/webhooks/...
 */
function extractAgentId(webhookUrl: string, node: INode): string {
	const match = webhookUrl.match(/\/agents\/([^/]+)\//);
	throwOperationErrorIf(!match?.[1], ERROR_MESSAGES.AGENT_INVALID_WEBHOOK_URL, node);
	return match?.[1] ?? '';
}

async function getAgentStatus(
	this: IExecuteFunctions,
	agentId: string,
	invocationId: string,
): Promise<AgentResultResponse> {
	const resultUrl = `https://api.airtop.ai/api/hooks/agents/${agentId}/invocations/${invocationId}/result`;
	const response = await apiRequest.call<
		IExecuteFunctions,
		['GET', string],
		Promise<AgentResultResponse>
	>(this, 'GET', resultUrl);
	return response;
}

/**
 * Polls the agent execution status until it completes or fails
 */
async function pollAgentStatus(
	this: IExecuteFunctions,
	agentId: string,
	invocationId: string,
	timeoutSeconds: number,
): Promise<AgentResultResponse | undefined> {
	const airtopNode = this.getNode();
	const startTime = Date.now();
	const timeoutMs = timeoutSeconds * 1000;
	let response: AgentResultResponse | undefined;

	this.logger.info(`[${airtopNode.name}] Polling agent status for invocationId: ${invocationId}`);

	while (!response?.output && !response?.error) {
		const elapsed = Date.now() - startTime;
		throwOperationErrorIf(elapsed >= timeoutMs, ERROR_MESSAGES.TIMEOUT_REACHED, airtopNode);

		response = await getAgentStatus.call(this, agentId, invocationId);

		if (response?.output || response?.error) {
			return response;
		}

		// Wait one second before next poll
		await new Promise((resolve) => setTimeout(resolve, 1000));
	}

	return {
		status: 'Unknown',
		output: {},
	};
}

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const airtopNode = this.getNode();
	const webhookUrl = validateRequiredStringField.call(this, index, 'webhookUrl', 'Webhook URL');
	const agentParametersJson = validateRequiredStringField.call(
		this,
		index,
		'agentParameters',
		'Parameters',
	);
	const agentId = extractAgentId(webhookUrl, airtopNode);
	const awaitExecution = this.getNodeParameter('awaitExecution', index, true) as boolean;
	const timeout = this.getNodeParameter('timeout', index, 600) as number;

	// Validate timeout
	throwOperationErrorIf(
		timeout < AGENT_MIN_TIMEOUT_SECONDS,
		ERROR_MESSAGES.AGENT_TIMEOUT_INVALID,
		airtopNode,
	);

	const invocationResponse = await apiRequest.call<
		IExecuteFunctions,
		['POST', string, IDataObject],
		Promise<AgentInvocationResponse>
	>(this, 'POST', webhookUrl, jsonParse<IDataObject>(agentParametersJson));

	const invocationId = invocationResponse.invocationId;
	throwOperationErrorIf(
		!invocationId,
		"No 'invocationId' received from agent webhook response",
		airtopNode,
	);

	if (!awaitExecution) {
		return this.helpers.returnJsonArray({
			invocationId,
		});
	}

	// Poll for agent's execution status
	const result = await pollAgentStatus.call(this, agentId, invocationId, timeout);
	throwOperationErrorIf(
		Boolean(result?.error),
		`${result?.error ?? 'Unknown error'}. Agent Invocation ID: ${invocationId}`,
		airtopNode,
	);

	return this.helpers.returnJsonArray({
		invocationId,
		status: result?.status ?? 'Unknown',
		output: result?.output ?? {},
	});
}
