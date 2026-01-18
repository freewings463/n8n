"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/actions/file/update/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/BambooHr/v1 的节点。导入/依赖:外部:无；内部:无；本地:../../Interfaces。导出:fileUpdateDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/actions/file/update/description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/actions/file/update/description.py

import type { FileProperties } from '../../Interfaces';

export const fileUpdateDescription: FileProperties = [
	{
		displayName: 'File ID',
		name: 'fileId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['file'],
			},
		},
		default: '',
		description: 'ID of the file',
	},
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['file'],
			},
		},
		options: [
			{
				displayName: 'Category Name or ID',
				name: 'categoryId',
				type: 'options',
				typeOptions: {
					loadOptionsMethod: 'getCompanyFileCategories',
				},
				default: '',
				description:
					'Move the file to a different category. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
			},
			{
				displayName: 'Name',
				name: 'name',
				type: 'string',
				default: '',
				description: 'New name of the file',
			},
			{
				displayName: 'Share with Employee',
				name: 'shareWithEmployee',
				type: 'boolean',
				default: true,
				description: 'Whether this file is shared or not',
			},
		],
	},
];
