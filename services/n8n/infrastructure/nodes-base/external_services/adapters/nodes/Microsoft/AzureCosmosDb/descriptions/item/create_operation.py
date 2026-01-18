"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/AzureCosmosDb/descriptions/item/create.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/AzureCosmosDb 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/utils、../common。导出:description。关键函数/方法:function。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/AzureCosmosDb/descriptions/item/create.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/AzureCosmosDb/descriptions/item/create_operation.py

import type {
	IDataObject,
	IExecuteSingleFunctions,
	IHttpRequestOptions,
	INodeProperties,
} from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import { processJsonInput, untilContainerSelected } from '../../helpers/utils';
import { containerResourceLocator } from '../common';

const properties: INodeProperties[] = [
	{ ...containerResourceLocator, description: 'Select the container you want to use' },
	{
		displayName: 'Item Contents',
		name: 'customProperties',
		default: '{\n\t"id": "replace_with_new_document_id"\n}',
		description: 'The item contents as a JSON object',
		displayOptions: {
			hide: {
				...untilContainerSelected,
			},
		},
		hint: 'The item requires an ID and partition key value if a custom key is set',
		required: true,
		routing: {
			send: {
				preSend: [
					async function (
						this: IExecuteSingleFunctions,
						requestOptions: IHttpRequestOptions,
					): Promise<IHttpRequestOptions> {
						const rawCustomProperties = this.getNodeParameter('customProperties') as IDataObject;
						const customProperties = processJsonInput(
							rawCustomProperties,
							'Item Contents',
							undefined,
							['id'],
						);
						requestOptions.body = customProperties;
						return requestOptions;
					},
				],
			},
		},
		type: 'json',
	},
];

const displayOptions = {
	show: {
		resource: ['item'],
		operation: ['create'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);
