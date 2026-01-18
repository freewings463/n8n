"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/memory/MemoryBufferWindow/MemoryBufferWindow.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/memory/MemoryBufferWindow 的节点。导入/依赖:外部:@langchain/classic/memory、@utils/helpers、@utils/logWrapper、@utils/sharedFields；内部:无；本地:无。导出:MemoryBufferWindow。关键函数/方法:getInstance、getMemory、cleanupStaleBuffers、getConnectionHintNoticeField、expressionSessionKeyProperty、supplyData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/memory/MemoryBufferWindow/MemoryBufferWindow.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/memory/MemoryBufferWindow/MemoryBufferWindow_node.py

import type { BufferWindowMemoryInput } from '@langchain/classic/memory';
import { BufferWindowMemory } from '@langchain/classic/memory';
import {
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeDescription,
	type ISupplyDataFunctions,
	type SupplyData,
} from 'n8n-workflow';

import { getSessionId } from '@utils/helpers';
import { logWrapper } from '@utils/logWrapper';
import { getConnectionHintNoticeField } from '@utils/sharedFields';

import {
	sessionIdOption,
	sessionKeyProperty,
	contextWindowLengthProperty,
	expressionSessionKeyProperty,
} from '../descriptions';

class MemoryChatBufferSingleton {
	private static instance: MemoryChatBufferSingleton;

	private memoryBuffer: Map<
		string,
		{ buffer: BufferWindowMemory; created: Date; last_accessed: Date }
	>;

	private constructor() {
		this.memoryBuffer = new Map();
	}

	static getInstance(): MemoryChatBufferSingleton {
		if (!MemoryChatBufferSingleton.instance) {
			MemoryChatBufferSingleton.instance = new MemoryChatBufferSingleton();
		}
		return MemoryChatBufferSingleton.instance;
	}

	async getMemory(
		sessionKey: string,
		memoryParams: BufferWindowMemoryInput,
	): Promise<BufferWindowMemory> {
		await this.cleanupStaleBuffers();

		let memoryInstance = this.memoryBuffer.get(sessionKey);
		if (memoryInstance) {
			memoryInstance.last_accessed = new Date();
		} else {
			const newMemory = new BufferWindowMemory(memoryParams);

			memoryInstance = {
				buffer: newMemory,
				created: new Date(),
				last_accessed: new Date(),
			};
			this.memoryBuffer.set(sessionKey, memoryInstance);
		}
		return memoryInstance.buffer;
	}

	private async cleanupStaleBuffers(): Promise<void> {
		const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000);

		for (const [key, memoryInstance] of this.memoryBuffer.entries()) {
			if (memoryInstance.last_accessed < oneHourAgo) {
				await this.memoryBuffer.get(key)?.buffer.clear();
				this.memoryBuffer.delete(key);
			}
		}
	}
}

export class MemoryBufferWindow implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Simple Memory',
		name: 'memoryBufferWindow',
		icon: 'fa:database',
		iconColor: 'black',
		group: ['transform'],
		version: [1, 1.1, 1.2, 1.3],
		description: 'Stores in n8n memory, so no credentials required',
		defaults: {
			name: 'Simple Memory',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Memory'],
				Memory: ['For beginners'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.memorybufferwindow/',
					},
				],
			},
		},

		inputs: [],

		outputs: [NodeConnectionTypes.AiMemory],
		outputNames: ['Memory'],
		properties: [
			getConnectionHintNoticeField([NodeConnectionTypes.AiAgent]),
			{
				displayName:
					'This node stores memory locally in the n8n instance. It is not compatible with Queue Mode or Multi-Main setups, as memory will not be shared across workers. For production use with scaling, consider using an external memory store such as Redis, Postgres, or another persistent memory node.',
				name: 'scalingNotice',
				type: 'notice',
				default: '',
			},
			{
				displayName: 'Session Key',
				name: 'sessionKey',
				type: 'string',
				default: 'chat_history',
				description: 'The key to use to store the memory in the workflow data',
				displayOptions: {
					show: {
						'@version': [1],
					},
				},
			},
			{
				displayName: 'Session ID',
				name: 'sessionKey',
				type: 'string',
				default: '={{ $json.sessionId }}',
				description: 'The key to use to store the memory',
				displayOptions: {
					show: {
						'@version': [1.1],
					},
				},
			},
			{
				...sessionIdOption,
				displayOptions: {
					show: {
						'@version': [{ _cnd: { gte: 1.2 } }],
					},
				},
			},
			expressionSessionKeyProperty(1.3),
			sessionKeyProperty,
			contextWindowLengthProperty,
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		const contextWindowLength = this.getNodeParameter('contextWindowLength', itemIndex) as number;
		const workflowId = this.getWorkflow().id;
		const memoryInstance = MemoryChatBufferSingleton.getInstance();

		const nodeVersion = this.getNode().typeVersion;

		let sessionId;

		if (nodeVersion >= 1.2) {
			sessionId = getSessionId(this, itemIndex);
		} else {
			sessionId = this.getNodeParameter('sessionKey', itemIndex) as string;
		}

		const memory = await memoryInstance.getMemory(`${workflowId}__${sessionId}`, {
			k: contextWindowLength,
			inputKey: 'input',
			memoryKey: 'chat_history',
			outputKey: 'output',
			returnMessages: true,
		});

		return {
			response: logWrapper(memory, this),
		};
	}
}
