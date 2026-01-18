"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Drive/v2/actions/folder/deleteFolder.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Drive 的节点。导入/依赖:外部:@utils/utilities；内部:n8n-workflow；本地:../../transport、../common.descriptions。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Drive/v2/actions/folder/deleteFolder.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Drive/v2/actions/folder/deleteFolder_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import { googleApiRequest } from '../../transport';
import { folderNoRootRLC } from '../common.descriptions';

const properties: INodeProperties[] = [
	{
		...folderNoRootRLC,
		description: 'The folder to delete',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		options: [
			{
				displayName: 'Delete Permanently',
				name: 'deletePermanently',
				type: 'boolean',
				default: false,
				description:
					'Whether to delete the folder immediately. If false, the folder will be moved to the trash.',
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['folder'],
		operation: ['deleteFolder'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const returnData: INodeExecutionData[] = [];

	const folderId = this.getNodeParameter('folderNoRootId', i, undefined, {
		extractValue: true,
	}) as string;

	const deletePermanently = this.getNodeParameter('options.deletePermanently', i, false) as boolean;

	const qs = {
		supportsAllDrives: true,
	};

	if (deletePermanently) {
		await googleApiRequest.call(this, 'DELETE', `/drive/v3/files/${folderId}`, undefined, qs);
	} else {
		await googleApiRequest.call(
			this,
			'PATCH',
			`/drive/v3/files/${folderId}`,
			{ trashed: true },
			qs,
		);
	}

	const executionData = this.helpers.constructExecutionMetaData(
		this.helpers.returnJsonArray({
			fileId: folderId,
			success: true,
		}),
		{ itemData: { item: i } },
	);

	returnData.push(...executionData);

	return returnData;
}
