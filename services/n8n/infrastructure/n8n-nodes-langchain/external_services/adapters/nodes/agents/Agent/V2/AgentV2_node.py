"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/V2/AgentV2.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../V2/description、../V2/execute、../utils。导出:AgentV2。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/V2/AgentV2.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/V2/AgentV2_node.py

import { NodeConnectionTypes } from 'n8n-workflow';
import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	INodeTypeBaseDescription,
} from 'n8n-workflow';

import {
	promptTypeOptionsDeprecated,
	textFromGuardrailsNode,
	textFromPreviousNode,
	textInput,
} from '@utils/descriptions';

import { getToolsAgentProperties } from '../agents/ToolsAgent/V2/description';
import { toolsAgentExecute } from '../agents/ToolsAgent/V2/execute';
import { getInputs } from '../utils';

export class AgentV2 implements INodeType {
	description: INodeTypeDescription;

	constructor(baseDescription: INodeTypeBaseDescription) {
		this.description = {
			...baseDescription,
			version: [2, 2.1, 2.2],
			defaults: {
				name: 'AI Agent',
				color: '#404040',
			},
			inputs: `={{
				((hasOutputParser, needsFallback) => {
					${getInputs.toString()};
					return getInputs(true, hasOutputParser, needsFallback);
				})($parameter.hasOutputParser === undefined || $parameter.hasOutputParser === true, $parameter.needsFallback !== undefined && $parameter.needsFallback === true)
			}}`,
			outputs: [NodeConnectionTypes.Main],
			properties: [
				{
					displayName:
						'Tip: Get a feel for agents with our quick <a href="https://docs.n8n.io/advanced-ai/intro-tutorial/" target="_blank">tutorial</a> or see an <a href="/workflows/templates/1954" target="_blank">example</a> of how this node works',
					name: 'aiAgentStarterCallout',
					type: 'callout',
					default: '',
				},
				promptTypeOptionsDeprecated,
				{
					...textFromGuardrailsNode,
					displayOptions: {
						show: {
							promptType: ['guardrails'],
						},
					},
				},
				{
					...textFromPreviousNode,
					displayOptions: {
						show: {
							promptType: ['auto'],
						},
					},
				},
				{
					...textInput,
					displayOptions: {
						show: {
							promptType: ['define'],
						},
					},
				},
				{
					displayName: 'Require Specific Output Format',
					name: 'hasOutputParser',
					type: 'boolean',
					default: false,
					noDataExpression: true,
				},
				{
					displayName: `Connect an <a data-action='openSelectiveNodeCreator' data-action-parameter-connectiontype='${NodeConnectionTypes.AiOutputParser}'>output parser</a> on the canvas to specify the output format you require`,
					name: 'notice',
					type: 'notice',
					default: '',
					displayOptions: {
						show: {
							hasOutputParser: [true],
						},
					},
				},
				{
					displayName: 'Enable Fallback Model',
					name: 'needsFallback',
					type: 'boolean',
					default: false,
					noDataExpression: true,
					displayOptions: {
						show: {
							'@version': [{ _cnd: { gte: 2.1 } }],
						},
					},
				},
				{
					displayName:
						'Connect an additional language model on the canvas to use it as a fallback if the main model fails',
					name: 'fallbackNotice',
					type: 'notice',
					default: '',
					displayOptions: {
						show: {
							needsFallback: [true],
						},
					},
				},
				...getToolsAgentProperties({ withStreaming: true }),
			],
			hints: [
				{
					message:
						'You are using streaming responses. Make sure to set the response mode to "Streaming Response" on the connected trigger node.',
					type: 'warning',
					location: 'outputPane',
					whenToDisplay: 'afterExecution',
					displayCondition: '={{ $parameter["enableStreaming"] === true }}',
				},
			],
		};
	}

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		return await toolsAgentExecute.call(this);
	}
}
