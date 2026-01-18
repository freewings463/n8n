"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/tools/ToolVectorStore/ToolVectorStore.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/tools/ToolVectorStore 的Store。导入/依赖:外部:@langchain/core/…/base、@langchain/core/vectorstores、@langchain/classic/chains、@langchain/classic/tools、@utils/logWrapper、@utils/sharedFields；内部:n8n-workflow；本地:无。导出:ToolVectorStore。关键函数/方法:execute、getTool、vectorStore、llm、getConnectionHintNoticeField、supplyData。用于管理该模块前端状态（state/actions/getters）供UI消费。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/tools/ToolVectorStore/ToolVectorStore.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/tools/ToolVectorStore/ToolVectorStore_node.py

import type { BaseLanguageModel } from '@langchain/core/language_models/base';
import type { VectorStore } from '@langchain/core/vectorstores';
import { VectorDBQAChain } from '@langchain/classic/chains';
import { VectorStoreQATool } from '@langchain/classic/tools';
import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	ISupplyDataFunctions,
	SupplyData,
} from 'n8n-workflow';
import { NodeConnectionTypes, nodeNameToToolName } from 'n8n-workflow';

import { logWrapper } from '@utils/logWrapper';
import { getConnectionHintNoticeField } from '@utils/sharedFields';

async function getTool(
	ctx: ISupplyDataFunctions | IExecuteFunctions,
	itemIndex: number,
): Promise<VectorStoreQATool> {
	const node = ctx.getNode();
	const { typeVersion } = node;
	const name =
		typeVersion <= 1
			? (ctx.getNodeParameter('name', itemIndex) as string)
			: nodeNameToToolName(node);
	const toolDescription = ctx.getNodeParameter('description', itemIndex) as string;
	const topK = ctx.getNodeParameter('topK', itemIndex, 4) as number;
	const description = VectorStoreQATool.getDescription(name, toolDescription);
	const vectorStore = (await ctx.getInputConnectionData(
		NodeConnectionTypes.AiVectorStore,
		itemIndex,
	)) as VectorStore;
	const llm = (await ctx.getInputConnectionData(
		NodeConnectionTypes.AiLanguageModel,
		itemIndex,
	)) as BaseLanguageModel;

	const vectorStoreTool = new VectorStoreQATool(name, description, {
		llm,
		vectorStore,
	});

	vectorStoreTool.chain = VectorDBQAChain.fromLLM(llm, vectorStore, {
		k: topK,
	});

	return vectorStoreTool;
}

export class ToolVectorStore implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Vector Store Question Answer Tool',
		name: 'toolVectorStore',
		icon: 'fa:database',
		iconColor: 'black',
		group: ['transform'],
		version: [1, 1.1],
		description: 'Answer questions with a vector store',
		defaults: {
			name: 'Answer questions with a vector store',
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
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolvectorstore/',
					},
				],
			},
		},

		inputs: [
			{
				displayName: 'Vector Store',
				maxConnections: 1,
				type: NodeConnectionTypes.AiVectorStore,
				required: true,
			},
			{
				displayName: 'Model',
				maxConnections: 1,
				type: NodeConnectionTypes.AiLanguageModel,
				required: true,
			},
		],

		outputs: [NodeConnectionTypes.AiTool],
		outputNames: ['Tool'],
		properties: [
			getConnectionHintNoticeField([NodeConnectionTypes.AiAgent]),
			{
				displayName: 'Data Name',
				name: 'name',
				type: 'string',
				default: '',
				placeholder: 'e.g. users_info',
				validateType: 'string-alphanumeric',
				description:
					'Name of the data in vector store. This will be used to fill this tool description: Useful for when you need to answer questions about [name]. Whenever you need information about [data description], you should ALWAYS use this. Input should be a fully formed question.',
				displayOptions: {
					show: {
						'@version': [1],
					},
				},
			},
			{
				displayName: 'Description of Data',
				name: 'description',
				type: 'string',
				default: '',
				placeholder: "[Describe your data here, e.g. a user's name, email, etc.]",
				description:
					'Describe the data in vector store. This will be used to fill this tool description: Useful for when you need to answer questions about [name]. Whenever you need information about [data description], you should ALWAYS use this. Input should be a fully formed question.',
				typeOptions: {
					rows: 3,
				},
			},
			{
				displayName: 'Limit',
				name: 'topK',
				type: 'number',
				default: 4,
				description: 'The maximum number of results to return',
			},
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		const vectorStoreTool = await getTool(this, itemIndex);

		return {
			response: logWrapper(vectorStoreTool, this),
		};
	}

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const inputData = this.getInputData();
		const result: INodeExecutionData[] = [];
		for (let itemIndex = 0; itemIndex < inputData.length; itemIndex++) {
			const tool = await getTool(this, itemIndex);
			const outputData = await tool.invoke(inputData[itemIndex].json);
			result.push({
				json: {
					response: outputData,
				},
				pairedItem: {
					item: itemIndex,
				},
			});
		}

		return [result];
	}
}
