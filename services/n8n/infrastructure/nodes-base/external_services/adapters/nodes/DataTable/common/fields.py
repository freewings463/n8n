"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DataTable/common/fields.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DataTable/common 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:DATA_TABLE_ID_FIELD、DRY_RUN、DATA_TABLE_RESOURCE_LOCATOR_BASE。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DataTable/common/fields.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DataTable/common/fields.py

import type { INodeProperties } from 'n8n-workflow';

export const DATA_TABLE_ID_FIELD = 'dataTableId';

export const DRY_RUN = {
	displayName: 'Dry Run',
	name: 'dryRun',
	type: 'boolean',
	default: false,
	description:
		'Whether the operation simulates and returns affected rows in their "before" and "after" states',
} satisfies INodeProperties;

export const DATA_TABLE_RESOURCE_LOCATOR_BASE = {
	// eslint-disable-next-line n8n-nodes-base/node-param-display-name-miscased
	displayName: 'Data table',
	name: DATA_TABLE_ID_FIELD,
	type: 'resourceLocator',
	default: { mode: 'list', value: '' },
	required: true,
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'tableSearch',
				searchable: true,
			},
		},
		{
			displayName: 'By Name',
			name: 'name',
			type: 'string',
			placeholder: 'e.g. My Table',
		},
		{
			displayName: 'ID',
			name: 'id',
			type: 'string',
		},
	],
} as const satisfies Omit<INodeProperties, 'displayOptions'>;
