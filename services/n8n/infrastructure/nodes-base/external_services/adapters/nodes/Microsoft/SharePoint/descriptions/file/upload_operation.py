"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/SharePoint/descriptions/file/upload.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/SharePoint 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/utils、../common.descriptions。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/SharePoint/descriptions/file/upload.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/SharePoint/descriptions/file/upload_operation.py

import { updateDisplayOptions, type INodeProperties } from 'n8n-workflow';

import { uploadFilePreSend } from '../../helpers/utils';
import { folderRLC, siteRLC, untilSiteSelected } from '../common.descriptions';

const properties: INodeProperties[] = [
	{
		...siteRLC,
		description: 'Select the site to retrieve folders from',
	},
	{
		...folderRLC,
		description: 'Select the folder to upload the file to',
		displayOptions: {
			hide: {
				...untilSiteSelected,
			},
		},
	},
	{
		displayName: 'File Name',
		name: 'fileName',
		default: '',
		description: 'The name of the file being uploaded',
		placeholder: 'e.g. My New File',
		required: true,
		type: 'string',
	},
	{
		displayName: 'File Contents',
		name: 'fileContents',
		default: '',
		description:
			'Find the name of input field containing the binary data to upload in the Input panel on the left, in the Binary tab',
		hint: 'The name of the input field containing the binary file data to upload',
		placeholder: 'data',
		required: true,
		routing: {
			send: {
				preSend: [uploadFilePreSend],
			},
		},
		type: 'string',
	},
];

const displayOptions = {
	show: {
		resource: ['file'],
		operation: ['upload'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);
