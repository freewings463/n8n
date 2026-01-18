"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v2/actions/asset/getPublicURL.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v2 的节点。导入/依赖:外部:无；内部:无；本地:../../GenericFunctions。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v2/actions/asset/getPublicURL.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v2/actions/asset/getPublicURL_operation.py

import {
	type IDataObject,
	type INodeExecutionData,
	type INodeProperties,
	type IExecuteFunctions,
	updateDisplayOptions,
} from 'n8n-workflow';

import { seaTableApiRequest } from '../../GenericFunctions';

const properties: INodeProperties[] = [
	{
		displayName: 'Asset Path',
		name: 'assetPath',
		type: 'string',
		placeholder: '/images/2023-09/logo.png',
		required: true,
		default: '',
	},
];

const displayOptions = {
	show: {
		resource: ['asset'],
		operation: ['getPublicURL'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const assetPath = this.getNodeParameter('assetPath', index) as string;

	let responseData = [] as IDataObject[];
	if (assetPath) {
		responseData = await seaTableApiRequest.call(
			this,
			{},
			'GET',
			`/api/v2.1/dtable/app-download-link/?path=${assetPath}`,
		);
	}

	return this.helpers.returnJsonArray(responseData);
}
