"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/utils/output_parsers/N8nOutputParser.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/utils/output_parsers 的工具。导入/依赖:外部:无；内部:n8n-workflow；本地:./N8nItemListOutputParser、./N8nOutputFixingParser、./N8nStructuredOutputParser。导出:N8nOutputParser、N8nOutputFixingParser、N8nItemListOutputParser、N8nStructuredOutputParser。关键函数/方法:getOptionalOutputParser。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/utils/output_parsers/N8nOutputParser.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/utils/output_parsers/N8nOutputParser.py

import type { IExecuteFunctions, ISupplyDataFunctions } from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { N8nItemListOutputParser } from './N8nItemListOutputParser';
import { N8nOutputFixingParser } from './N8nOutputFixingParser';
import { N8nStructuredOutputParser } from './N8nStructuredOutputParser';

export type N8nOutputParser =
	| N8nOutputFixingParser
	| N8nStructuredOutputParser
	| N8nItemListOutputParser;

export { N8nOutputFixingParser, N8nItemListOutputParser, N8nStructuredOutputParser };

export async function getOptionalOutputParser(
	ctx: IExecuteFunctions | ISupplyDataFunctions,
	index: number = 0,
): Promise<N8nOutputParser | undefined> {
	let outputParser: N8nOutputParser | undefined;

	if (ctx.getNodeParameter('hasOutputParser', 0, true) === true) {
		outputParser = (await ctx.getInputConnectionData(
			NodeConnectionTypes.AiOutputParser,
			index,
		)) as N8nOutputParser;
	}

	return outputParser;
}
