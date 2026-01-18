"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/tools/ToolThink/ToolThink.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/tools/ToolThink 的节点。导入/依赖:外部:@langchain/classic/tools、@utils/logWrapper、@utils/sharedFields；内部:无；本地:无。导出:ToolThink。关键函数/方法:execute、getTool、getConnectionHintNoticeField、supplyData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/tools/ToolThink/ToolThink.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/tools/ToolThink/ToolThink_node.py

import { DynamicTool } from '@langchain/classic/tools';
import {
	type IExecuteFunctions,
	NodeConnectionTypes,
	nodeNameToToolName,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
	type INodeExecutionData,
} from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';
import { getConnectionHintNoticeField } from '@utils/sharedFields';

async function getTool(
	ctx: ISupplyDataFunctions | IExecuteFunctions,
	itemIndex: number,
): Promise<DynamicTool> {
	const node = ctx.getNode();
	const { typeVersion } = node;

	const name = typeVersion === 1 ? 'thinking_tool' : nodeNameToToolName(node);
	const description = ctx.getNodeParameter('description', itemIndex) as string;

	return new DynamicTool({
		name,
		description,
		func: async (subject: string) => {
			return subject;
		},
	});
}

// A thinking tool, see https://www.anthropic.com/engineering/claude-think-tool

const defaultToolDescription =
	'Use the tool to think about something. It will not obtain new information or change the database, but just append the thought to the log. Use it when complex reasoning or some cache memory is needed.';

export class ToolThink implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Think Tool',
		name: 'toolThink',
		icon: 'fa:brain',
		iconColor: 'black',
		group: ['transform'],
		version: [1, 1.1],
		description: 'Invite the AI agent to do some thinking',
		defaults: {
			name: 'Think',
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
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolthink/',
					},
				],
			},
		},
		inputs: [],
		outputs: [NodeConnectionTypes.AiTool],
		outputNames: ['Tool'],
		properties: [
			getConnectionHintNoticeField([NodeConnectionTypes.AiAgent]),
			{
				displayName: 'Think Tool Description',
				name: 'description',
				type: 'string',
				default: defaultToolDescription,
				placeholder: '[Describe your thinking tool here, explaining how it will help the AI think]',
				description: "The thinking tool's description",
				typeOptions: {
					rows: 3,
				},
				required: true,
			},
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		const tool = await getTool(this, itemIndex);

		return {
			response: logWrapper(tool, this),
		};
	}

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const input = this.getInputData();
		const response: INodeExecutionData[] = [];
		for (let i = 0; i < input.length; i++) {
			const inputItem = input[i];
			const tool = await getTool(this, i);
			const result = await tool.invoke(inputItem.json);
			response.push({
				json: {
					response: result,
				},
				pairedItem: {
					item: i,
				},
			});
		}

		return [response];
	}
}
