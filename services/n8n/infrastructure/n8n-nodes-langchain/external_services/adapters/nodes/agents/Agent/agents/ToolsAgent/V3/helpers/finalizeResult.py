"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/finalizeResult.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:@langchain/classic/memory、lodash/omit、@utils/output_parsers/N8nOutputParser；内部:n8n-workflow；本地:../types。导出:finalizeResult。关键函数/方法:finalizeResult。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/finalizeResult.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/agents/ToolsAgent/V3/helpers/finalizeResult.py

import type { BaseChatMemory } from '@langchain/classic/memory';
import omit from 'lodash/omit';
import { jsonParse } from 'n8n-workflow';
import type { INodeExecutionData } from 'n8n-workflow';

import type { N8nOutputParser } from '@utils/output_parsers/N8nOutputParser';

import type { AgentResult } from '../types';

/**
 * Finalizes the result by parsing output and preparing execution data.
 * Handles output parser integration and memory-based parsing.
 *
 * @param result - The agent result to finalize
 * @param itemIndex - The current item index
 * @param memory - Optional memory for parsing context
 * @param outputParser - Optional output parser for structured responses
 * @returns INodeExecutionData ready for output
 */
export function finalizeResult(
	result: AgentResult,
	itemIndex: number,
	memory: BaseChatMemory | undefined,
	outputParser: N8nOutputParser | undefined,
): INodeExecutionData {
	// If memory and outputParser are connected, parse the output.
	if (memory && outputParser) {
		const parsedOutput = jsonParse<{ output: Record<string, unknown> }>(result.output);
		// Type assertion needed because parsedOutput can be various types
		result.output = (parsedOutput?.output ?? parsedOutput) as unknown as string;
	}

	// Omit internal keys before returning the result.
	const itemResult: INodeExecutionData = {
		json: omit(
			result,
			'system_message',
			'formatting_instructions',
			'input',
			'chat_history',
			'agent_scratchpad',
		),
		pairedItem: { item: itemIndex },
	};

	return itemResult;
}
