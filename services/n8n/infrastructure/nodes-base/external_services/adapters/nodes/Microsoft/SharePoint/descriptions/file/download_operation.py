"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/SharePoint/descriptions/file/download.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/SharePoint 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/SharePoint/descriptions/file/download.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/SharePoint/descriptions/file/download_operation.py

import { updateDisplayOptions, type INodeProperties } from 'n8n-workflow';

import {
	fileRLC,
	folderRLC,
	siteRLC,
	untilFolderSelected,
	untilSiteSelected,
} from '../common.descriptions';

const properties: INodeProperties[] = [
	{
		...siteRLC,
		description: 'Select the site to retrieve folders from',
	},
	{
		...folderRLC,
		description: 'Select the folder to download the file from',
		displayOptions: {
			hide: {
				...untilSiteSelected,
			},
		},
	},
	{
		...fileRLC,
		description: 'Select the file to download',
		displayOptions: {
			hide: {
				...untilSiteSelected,
				...untilFolderSelected,
			},
		},
	},
];

const displayOptions = {
	show: {
		resource: ['file'],
		operation: ['download'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);
