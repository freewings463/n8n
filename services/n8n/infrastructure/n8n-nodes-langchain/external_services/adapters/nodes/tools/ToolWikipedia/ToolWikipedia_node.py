"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/tools/ToolWikipedia/ToolWikipedia.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/tools/ToolWikipedia 的节点。导入/依赖:外部:@langchain/community/…/wikipedia_query_run、@utils/logWrapper、@utils/sharedFields；内部:无；本地:无。导出:ToolWikipedia。关键函数/方法:execute、getTool、supplyData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/tools/ToolWikipedia/ToolWikipedia.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/tools/ToolWikipedia/ToolWikipedia_node.py

import { WikipediaQueryRun } from '@langchain/community/tools/wikipedia_query_run';
import {
	type IExecuteFunctions,
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
	type INodeExecutionData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';
import { getConnectionHintNoticeField } from '@utils/sharedFields';

function getTool(ctx: ISupplyDataFunctions | IExecuteFunctions): WikipediaQueryRun {
	const WikiTool = new WikipediaQueryRun();
	WikiTool.name = ctx.getNode().name;
	WikiTool.description =
		'A tool for interacting with and fetching data from the Wikipedia API. The input should always be a string query.';
	return WikiTool;
}

export class ToolWikipedia implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Wikipedia',
		name: 'toolWikipedia',
		icon: 'file:wikipedia.svg',
		group: ['transform'],
		version: 1,
		description: 'Search in Wikipedia',
		defaults: {
			name: 'Wikipedia',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Tools'],
				Tools: ['Other Tools'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolwikipedia/',
					},
				],
			},
		},

		inputs: [],

		outputs: [NodeConnectionTypes.AiTool],
		outputNames: ['Tool'],
		properties: [getConnectionHintNoticeField([NodeConnectionTypes.AiAgent])],
	};

	async supplyData(this: ISupplyDataFunctions): Promise<SupplyData> {
		return {
			response: logWrapper(getTool(this), this),
		};
	}

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const WikiTool = getTool(this);

		const items = this.getInputData();

		const response: INodeExecutionData[] = [];
		for (let itemIndex = 0; itemIndex < this.getInputData().length; itemIndex++) {
			const item = items[itemIndex];
			if (item === undefined) {
				continue;
			}
			const result = await WikiTool.invoke(item.json);
			response.push({
				json: { response: result },
				pairedItem: { item: itemIndex },
			});
		}

		return [response];
	}
}
