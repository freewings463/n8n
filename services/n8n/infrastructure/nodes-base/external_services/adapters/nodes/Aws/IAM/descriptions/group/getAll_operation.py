"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/IAM/descriptions/group/getAll.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/IAM 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../common。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/IAM/descriptions/group/getAll.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/IAM/descriptions/group/getAll_operation.py

import type { INodeProperties } from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import { paginationParameters } from '../common';

const properties: INodeProperties[] = [
	...paginationParameters,
	{
		displayName: 'Include Users',
		name: 'includeUsers',
		type: 'boolean',
		default: false,
		description: 'Whether to include a list of users in the group',
	},
];

const displayOptions = {
	show: {
		resource: ['group'],
		operation: ['getAll'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);
