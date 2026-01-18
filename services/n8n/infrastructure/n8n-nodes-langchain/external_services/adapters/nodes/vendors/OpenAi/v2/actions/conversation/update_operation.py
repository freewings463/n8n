"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v2/actions/conversation/update.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport、../descriptions。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v2/actions/conversation/update.operation.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/v2/actions/conversation/update_operation.py

import type {
	INodeProperties,
	IExecuteFunctions,
	INodeExecutionData,
	IDataObject,
} from 'n8n-workflow';
import { updateDisplayOptions, jsonParse } from 'n8n-workflow';

import { apiRequest } from '../../../transport';
import { metadataProperty } from '../descriptions';

const properties: INodeProperties[] = [
	{
		displayName: 'Conversation ID',
		name: 'conversationId',
		type: 'string',
		default: '',
		placeholder: 'conv_1234567890',
		description: 'The ID of the conversation to update',
		required: true,
	},
	{ ...metadataProperty, required: true },
];

const displayOptions = {
	show: {
		operation: ['update'],
		resource: ['conversation'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const conversationId = this.getNodeParameter('conversationId', i, '') as string;
	const metadata = this.getNodeParameter('metadata', i, '') as string;

	if (!conversationId) {
		throw new Error('Conversation ID is required');
	}

	if (!metadata) {
		throw new Error('Metadata is required');
	}

	const body: IDataObject = {};

	body.metadata = jsonParse(metadata, {
		errorMessage: 'Invalid JSON in metadata field',
	});

	const response = await apiRequest.call(this, 'POST', `/conversations/${conversationId}`, {
		body,
	});

	return [
		{
			json: response,
			pairedItem: { item: i },
		},
	];
}
