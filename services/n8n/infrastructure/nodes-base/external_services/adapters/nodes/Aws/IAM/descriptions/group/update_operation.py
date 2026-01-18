"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/IAM/descriptions/group/update.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/IAM 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/utils、../common。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/IAM/descriptions/group/update.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/IAM/descriptions/group/update_operation.py

import type { INodeProperties } from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import { validatePath } from '../../helpers/utils';
import { groupLocator, groupNameParameter, pathParameter } from '../common';

const properties: INodeProperties[] = [
	{
		...groupLocator,
		description: 'Select the group you want to update',
	},
	{
		...groupNameParameter,
		description: 'The new name of the group',
		placeholder: 'e.g. GroupName',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Option',
		default: {},
		options: [
			{
				...pathParameter,
				placeholder: 'e.g. /division_abc/engineering/',
				description: 'The new path to the group, if it is not included, it defaults to a slash (/)',
				routing: {
					send: {
						preSend: [validatePath],
						property: 'NewPath',
						type: 'query',
					},
				},
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['group'],
		operation: ['update'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);
