"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Simulate/descriptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Simulate 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:iconSelector、subtitleProperty、jsonOutputProperty、executionDurationProperty。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Simulate/descriptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Simulate/descriptions.py

import type { INodeProperties } from 'n8n-workflow';

export const iconSelector: INodeProperties = {
	// eslint-disable-next-line n8n-nodes-base/node-param-display-name-wrong-for-dynamic-options
	displayName: 'Icon to Display on Canvas',
	name: 'icon',
	type: 'options',
	// eslint-disable-next-line n8n-nodes-base/node-param-description-wrong-for-dynamic-options
	description: 'Select a type of node to show corresponding icon',
	default: 'n8n-nodes-base.noOp',
	typeOptions: {
		loadOptionsMethod: 'getNodeTypes',
	},
};

export const subtitleProperty: INodeProperties = {
	displayName: 'Subtitle',
	name: 'subtitle',
	type: 'string',
	default: '',
	placeholder: "e.g. 'record: read'",
};

export const jsonOutputProperty: INodeProperties = {
	displayName: 'JSON',
	name: 'jsonOutput',
	type: 'json',
	typeOptions: {
		rows: 5,
	},
	default: '[\n  {\n  "my_field_1": "value",\n  "my_field_2": 1\n  }\n]',
	validateType: 'array',
};

export const executionDurationProperty: INodeProperties = {
	displayName: 'Execution Duration (MS)',
	name: 'executionDuration',
	type: 'number',
	default: 150,
	description: 'Execution duration in milliseconds',
	typeOptions: {
		minValue: 0,
	},
};
