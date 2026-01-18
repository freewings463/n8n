"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/AzureCosmosDb/AzureCosmosDb.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/AzureCosmosDb 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./descriptions、./methods。导出:AzureCosmosDb。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/AzureCosmosDb/AzureCosmosDb.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/AzureCosmosDb/AzureCosmosDb_node.py

import type { INodeType, INodeTypeDescription } from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { container, item } from './descriptions';
import { listSearch } from './methods';

export class AzureCosmosDb implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Azure Cosmos DB',
		name: 'azureCosmosDb',
		icon: {
			light: 'file:AzureCosmosDb.svg',
			dark: 'file:AzureCosmosDb.svg',
		},
		group: ['transform'],
		version: 1,
		subtitle: '={{ $parameter["operation"] + ": " + $parameter["resource"] }}',
		description: 'Interact with Azure Cosmos DB API',
		defaults: {
			name: 'Azure Cosmos DB',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'microsoftAzureCosmosDbSharedKeyApi',
				required: true,
			},
		],
		requestDefaults: {
			baseURL:
				'=https://{{ $credentials.account }}.documents.azure.com/dbs/{{ $credentials.database }}',
			json: true,
			ignoreHttpStatusErrors: true,
		},
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Container',
						value: 'container',
					},
					{
						name: 'Item',
						value: 'item',
					},
				],
				default: 'container',
			},

			...container.description,
			...item.description,
		],
	};

	methods = {
		listSearch,
	};
}
