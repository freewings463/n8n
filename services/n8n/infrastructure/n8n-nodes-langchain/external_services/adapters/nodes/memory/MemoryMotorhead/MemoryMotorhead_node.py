"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/memory/MemoryMotorhead/MemoryMotorhead.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/memory/MemoryMotorhead 的节点。导入/依赖:外部:@langchain/community/…/motorhead_memory、@utils/helpers、@utils/logWrapper、@utils/sharedFields；内部:无；本地:../descriptions。导出:MemoryMotorhead。关键函数/方法:getConnectionHintNoticeField、expressionSessionKeyProperty、supplyData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/memory/MemoryMotorhead/MemoryMotorhead.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/memory/MemoryMotorhead/MemoryMotorhead_node.py

import { MotorheadMemory } from '@langchain/community/memory/motorhead_memory';
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

import { expressionSessionKeyProperty, sessionIdOption, sessionKeyProperty } from '../descriptions';

export class MemoryMotorhead implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Motorhead',
		name: 'memoryMotorhead',
		icon: 'fa:file-export',
		iconColor: 'black',
		group: ['transform'],
		version: [1, 1.1, 1.2, 1.3],
		description: 'Use Motorhead Memory',
		defaults: {
			name: 'Motorhead',
		},
		codex: {
			categories: ['AI'],
			subcategories: {
				AI: ['Memory'],
				Memory: ['Other memories'],
			},
			resources: {
				primaryDocumentation: [
					{
						url: 'https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.memorymotorhead/',
					},
				],
			},
		},

		inputs: [],

		outputs: [NodeConnectionTypes.AiMemory],
		outputNames: ['Memory'],
		credentials: [
			{
				name: 'motorheadApi',
				required: true,
			},
		],
		properties: [
			getConnectionHintNoticeField([NodeConnectionTypes.AiAgent]),
			{
				displayName: 'Session ID',
				name: 'sessionId',
				type: 'string',
				required: true,
				default: '',
				displayOptions: {
					show: {
						'@version': [1],
					},
				},
			},
			{
				displayName: 'Session ID',
				name: 'sessionId',
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
		],
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		const credentials = await this.getCredentials('motorheadApi');
		const nodeVersion = this.getNode().typeVersion;

		let sessionId;

		if (nodeVersion >= 1.2) {
			sessionId = getSessionId(this, itemIndex);
		} else {
			sessionId = this.getNodeParameter('sessionId', itemIndex) as string;
		}

		const memory = new MotorheadMemory({
			sessionId,
			url: `${credentials.host as string}/motorhead`,
			clientId: credentials.clientId as string,
			apiKey: credentials.apiKey as string,
			memoryKey: 'chat_history',
			returnMessages: true,
			inputKey: 'input',
			outputKey: 'output',
		});

		await memory.init();

		return {
			response: logWrapper(memory, this),
		};
	}
}
