"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SyncroMSP/v1/methods/sharedFields.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SyncroMSP/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:addressFixedCollection。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SyncroMSP/v1/methods/sharedFields.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SyncroMSP/v1/methods/sharedFields.py

import type { INodeProperties } from 'n8n-workflow';

export const addressFixedCollection: INodeProperties = {
	displayName: 'Address',
	name: 'address',
	placeholder: 'Add Address Fields',
	type: 'fixedCollection',
	default: {},
	options: [
		{
			displayName: 'Address Fields',
			name: 'addressFields',
			values: [
				{
					displayName: 'Line 1',
					name: 'address',
					type: 'string',
					default: '',
				},
				{
					displayName: 'Line 2',
					name: 'address2',
					type: 'string',
					default: '',
				},
				{
					displayName: 'City',
					name: 'city',
					type: 'string',
					default: '',
				},
				{
					displayName: 'State',
					name: 'state',
					type: 'string',
					default: '',
				},
				{
					displayName: 'ZIP',
					name: 'zip',
					type: 'string',
					default: '',
				},
			],
		},
	],
};
