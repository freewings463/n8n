"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/tools/ToolSearXng/ToolSearXng.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/tools/ToolSearXng 的节点。导入/依赖:外部:@langchain/community/…/searxng_search、@utils/logWrapper、@utils/sharedFields；内部:n8n-workflow；本地:无。导出:ToolSearXng。关键函数/方法:execute、getTool、getConnectionHintNoticeField、supplyData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/tools/ToolSearXng/ToolSearXng.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/tools/ToolSearXng/ToolSearXng_node.py

import { SearxngSearch } from '@langchain/community/tools/searxng_search';
import { NodeConnectionTypes } from 'n8n-workflow';
import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	ISupplyDataFunctions,
	SupplyData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';
import { getConnectionHintNoticeField } from '@utils/sharedFields';

type Options = {
	numResults: number;
	pageNumber: number;
	language: string;
	safesearch: 0 | 1 | 2;
};

async function getTool(ctx: ISupplyDataFunctions | IExecuteFunctions, itemIndex: number) {
	const credentials = await ctx.getCredentials<{ apiUrl: string }>('searXngApi');
	const options = ctx.getNodeParameter('options', itemIndex) as Options;

	return new SearxngSearch({
		apiBase: credentials.apiUrl,
		headers: {
			Accept: 'application/json',
		},
		params: options,
	});
}

export class ToolSearXng implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'SearXNG',
		name: 'toolSearXng',
		icon: 'file:searXng.svg',
		group: ['transform'],
		version: 1,
		description: 'Search in SearXNG',
		defaults: {
			name: 'SearXNG',
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
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolsearxng',
					},
				],
			},
		},
		inputs: [],
		outputs: [NodeConnectionTypes.AiTool],
		outputNames: ['Tool'],
		credentials: [
			{
				name: 'searXngApi',
				required: true,
			},
		],
		properties: [
			getConnectionHintNoticeField([NodeConnectionTypes.AiAgent]),
			{
				displayName: 'Options',
				name: 'options',
				type: 'collection',
				placeholder: 'Add Option',
				default: {},
				options: [
					{
						displayName: 'Number of Results',
						name: 'numResults',
						type: 'number',
						default: 10,
					},
					{
						displayName: 'Search Page Number',
						name: 'pageNumber',
						type: 'number',
						default: 1,
					},
					{
						displayName: 'Language',
						name: 'language',
						type: 'string',
						default: 'en',
						description:
							'Defines the language to use. It\'s a two-letter language code. (e.g., `en` for English, `es` for Spanish, or `fr` for French). Head to <a href="https://docs.searxng.org/user/search-syntax.html#select-language">SearXNG search syntax page</a> for more info.',
					},
					{
						displayName: 'Safe Search',
						name: 'safesearch',
						type: 'options',
						options: [
							{
								name: 'None',
								value: 0,
							},
							{
								name: 'Moderate',
								value: 1,
							},
							{
								name: 'Strict',
								value: 2,
							},
						],
						default: 0,
						description: 'Filter search results of engines which support safe search',
					},
				],
			},
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		return {
			response: logWrapper(await getTool(this, itemIndex), this),
		};
	}

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const result: INodeExecutionData[] = [];
		const input = this.getInputData();
		for (let i = 0; i < input.length; i++) {
			const item = input[i];
			const tool = await getTool(this, i);
			result.push({
				json: {
					response: await tool.invoke(item.json),
				},
				pairedItem: {
					item: i,
				},
			});
		}

		return [result];
	}
}
