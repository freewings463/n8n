"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Drive/v2/actions/file/share.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Drive 的节点。导入/依赖:外部:@utils/utilities；内部:无；本地:../../transport、../common.descriptions。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Drive/v2/actions/file/share.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Drive/v2/actions/file/share_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import { googleApiRequest } from '../../transport';
import { fileRLC, permissionsOptions, shareOptions } from '../common.descriptions';

const properties: INodeProperties[] = [
	{
		...fileRLC,
		description: 'The file to share',
	},
	permissionsOptions,
	shareOptions,
];

const displayOptions = {
	show: {
		resource: ['file'],
		operation: ['share'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const returnData: INodeExecutionData[] = [];

	const fileId = this.getNodeParameter('fileId', i, undefined, {
		extractValue: true,
	}) as string;

	const permissions = this.getNodeParameter('permissionsUi', i) as IDataObject;

	const shareOption = this.getNodeParameter('options', i);

	const body: IDataObject = {};

	const qs: IDataObject = {
		supportsAllDrives: true,
	};

	if (permissions.permissionsValues) {
		Object.assign(body, permissions.permissionsValues);
	}

	Object.assign(qs, shareOption);

	const response = await googleApiRequest.call(
		this,
		'POST',
		`/drive/v3/files/${fileId}/permissions`,
		body,
		qs,
	);

	const executionData = this.helpers.constructExecutionMetaData(
		this.helpers.returnJsonArray(response as IDataObject[]),
		{ itemData: { item: i } },
	);
	returnData.push(...executionData);

	return returnData;
}
