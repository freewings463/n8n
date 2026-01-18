"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/memory/MemoryChatRetriever/MemoryChatRetriever.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/memory/MemoryChatRetriever 的节点。导入/依赖:外部:@langchain/community/…/chat_memory、@langchain/core/messages；内部:无；本地:无。导出:MemoryChatRetriever。关键函数/方法:execute、simplifyMessages、memory。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/memory/MemoryChatRetriever/MemoryChatRetriever.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/memory/MemoryChatRetriever/MemoryChatRetriever_node.py

import type { BaseChatMemory } from '@langchain/community/memory/chat_memory';
import type { BaseMessage } from '@langchain/core/messages';
import {
	NodeConnectionTypes,
	type IDataObject,
	type IExecuteFunctions,
	type INodeExecutionData,
	type INodeType,
	type INodeTypeDescription,
} from 'n8n-workflow';

function simplifyMessages(messages: BaseMessage[]) {
	const chunkedMessages = [];
	for (let i = 0; i < messages.length; i += 2) {
		chunkedMessages.push([messages[i], messages[i + 1]]);
	}

	const transformedMessages = chunkedMessages.map((exchange) => {
		const simplified = {
			[exchange[0]._getType()]: exchange[0].content,
		};

		if (exchange[1]) {
			simplified[exchange[1]._getType()] = exchange[1].content;
		}

		return {
			json: simplified,
		};
	});
	return transformedMessages;
}

// This node is deprecated. Use MemoryManager instead.
export class MemoryChatRetriever implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Chat Messages Retriever',
		name: 'memoryChatRetriever',
		icon: 'fa:database',
		iconColor: 'black',
		group: ['transform'],
		hidden: true,
		version: 1,
		description: 'Retrieve chat messages from memory and use them in the workflow',
		defaults: {
			name: 'Chat Messages Retriever',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Miscellaneous'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.memorymanager/',
					},
				],
			},
		},

		inputs: [
			NodeConnectionTypes.Main,
			{
				displayName: 'Memory',
				maxConnections: 1,
				type: NodeConnectionTypes.AiMemory,
				required: true,
			},
		],

		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName: "This node is deprecated. Use 'Chat Memory Manager' node instead.",
				type: 'notice',
				default: '',
				name: 'deprecatedNotice',
			},
			{
				displayName: 'Simplify Output',
				name: 'simplifyOutput',
				type: 'boolean',
				description: 'Whether to simplify the output to only include the sender and the text',
				default: true,
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		this.logger.debug('Executing Chat Memory Retriever');

		const memory = (await this.getInputConnectionData(NodeConnectionTypes.AiMemory, 0)) as
			| BaseChatMemory
			| undefined;
		const simplifyOutput = this.getNodeParameter('simplifyOutput', 0) as boolean;

		const messages = await memory?.chatHistory.getMessages();

		if (simplifyOutput && messages) {
			return [simplifyMessages(messages)];
		}

		const serializedMessages =
			messages?.map((message) => {
				const serializedMessage = message.toJSON();
				return { json: serializedMessage as unknown as IDataObject };
			}) ?? [];

		return [serializedMessages];
	}
}
