"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Storage/AzureStorage.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Storage 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./descriptions、./GenericFunctions。导出:AzureStorage。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Storage/AzureStorage.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Storage/AzureStorage_node.py

import type { INodeType, INodeTypeDescription } from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { blobFields, blobOperations, containerFields, containerOperations } from './descriptions';
import { getBlobs, getContainers } from './GenericFunctions';

export class AzureStorage implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Azure Storage',
		name: 'azureStorage',
		icon: {
			light: 'file:azureStorage.svg',
			dark: 'file:azureStorage.dark.svg',
		},
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Interact with Azure Storage API',
		defaults: {
			name: 'Azure Storage',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'azureStorageOAuth2Api',
				required: true,
				displayOptions: {
					show: {
						authentication: ['oAuth2'],
					},
				},
			},
			{
				name: 'azureStorageSharedKeyApi',
				required: true,
				displayOptions: {
					show: {
						authentication: ['sharedKey'],
					},
				},
			},
		],
		requestDefaults: {
			baseURL: '={{ $credentials.baseUrl }}',
		},
		properties: [
			{
				displayName: 'Authentication',
				name: 'authentication',
				type: 'options',
				options: [
					{
						name: 'OAuth2',
						value: 'oAuth2',
					},
					{
						name: 'Shared Key',
						value: 'sharedKey',
					},
				],
				default: 'sharedKey',
			},
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Blob',
						value: 'blob',
					},
					{
						name: 'Container',
						value: 'container',
					},
				],
				default: 'container',
			},

			...blobOperations,
			...blobFields,
			...containerOperations,
			...containerFields,
		],
	};

	methods = {
		loadOptions: {},

		listSearch: {
			getBlobs,
			getContainers,
		},
	};
}
