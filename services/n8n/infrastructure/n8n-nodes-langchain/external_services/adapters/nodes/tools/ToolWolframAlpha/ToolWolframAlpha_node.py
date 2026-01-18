"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/tools/ToolWolframAlpha/ToolWolframAlpha.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/tools/ToolWolframAlpha 的节点。导入/依赖:外部:@langchain/community/…/wolframalpha、@utils/logWrapper、@utils/sharedFields；内部:无；本地:无。导出:ToolWolframAlpha。关键函数/方法:execute、supplyData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/tools/ToolWolframAlpha/ToolWolframAlpha.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/tools/ToolWolframAlpha/ToolWolframAlpha_node.py

import { WolframAlphaTool } from '@langchain/community/tools/wolframalpha';
import {
	NodeConnectionTypes,
	type IExecuteFunctions,
	type INodeExecutionData,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';
import { getConnectionHintNoticeField } from '@utils/sharedFields';

export class ToolWolframAlpha implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Wolfram|Alpha',
		name: 'toolWolframAlpha',
		icon: 'file:wolfram-alpha.svg',
		group: ['transform'],
		version: 1,
		description: "Connects to WolframAlpha's computational intelligence engine.",
		defaults: {
			name: 'Wolfram Alpha',
		},
		credentials: [
			{
				name: 'wolframAlphaApi',
				required: true,
			},
		],
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Tools'],
				Tools: ['Other Tools'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolwolframalpha/',
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
		const credentials = await this.getCredentials('wolframAlphaApi');

		return {
			response: logWrapper(new WolframAlphaTool({ appid: credentials.appId as string }), this),
		};
	}

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const credentials = await this.getCredentials('wolframAlphaApi');
		const input = this.getInputData();
		const result: INodeExecutionData[] = [];

		for (let i = 0; i < input.length; i++) {
			const item = input[i];
			const tool = new WolframAlphaTool({ appid: credentials.appId as string });
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
