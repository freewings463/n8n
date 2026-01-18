"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:@langchain/core/output_parsers、@langchain/classic/tools；内部:n8n-workflow；本地:../types/types。导出:无。关键函数/方法:extractParsedOutput、parsedOutput、checkForStructuredTools、getToolName。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/utils.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/agents/utils.py

import type { BaseOutputParser } from '@langchain/core/output_parsers';
import type { DynamicStructuredTool, Tool } from '@langchain/classic/tools';
import { NodeOperationError, type IExecuteFunctions, type INode } from 'n8n-workflow';

import type { ZodObjectAny } from '../../../../types/types';

export async function extractParsedOutput(
	ctx: IExecuteFunctions,
	outputParser: BaseOutputParser<unknown>,
	output: string,
): Promise<Record<string, unknown> | undefined> {
	const parsedOutput = (await outputParser.parse(output)) as {
		output: Record<string, unknown>;
	};

	if (ctx.getNode().typeVersion <= 1.6) {
		return parsedOutput;
	}
	// For 1.7 and above, we try to extract the output from the parsed output
	// with fallback to the original output if it's not present
	return parsedOutput?.output ?? parsedOutput;
}

export async function checkForStructuredTools(
	tools: Array<Tool | DynamicStructuredTool<ZodObjectAny>>,
	node: INode,
	currentAgentType: string,
) {
	const dynamicStructuredTools = tools.filter(
		(tool) => tool.constructor.name === 'DynamicStructuredTool',
	);
	if (dynamicStructuredTools.length > 0) {
		const getToolName = (tool: Tool | DynamicStructuredTool) => `"${tool.name}"`;
		throw new NodeOperationError(
			node,
			`The selected tools are not supported by "${currentAgentType}", please use "Tools Agent" instead`,
			{
				itemIndex: 0,
				description: `Incompatible connected tools: ${dynamicStructuredTools.map(getToolName).join(', ')}`,
			},
		);
	}
}
