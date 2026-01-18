"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v2/actions/base/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v2 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./collaborator.operation、./metadata.operation、./snapshot.operation。导出:snapshot、metadata、collaborator、descriptions。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v2/actions/base/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v2/actions/base/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as collaborator from './collaborator.operation';
import * as metadata from './metadata.operation';
import * as snapshot from './snapshot.operation';

export { snapshot, metadata, collaborator };

export const descriptions: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['base'],
			},
		},
		options: [
			{
				name: 'Snapshot',
				value: 'snapshot',
				description: 'Create a snapshot of the base',
				action: 'Create a snapshot',
			},
			{
				name: 'Metadata',
				value: 'metadata',
				description: 'Get the complete metadata of the base',
				action: 'Get metadata of a base',
			},
			{
				name: 'Collaborator',
				value: 'collaborator',
				description: 'Get the username from the email or name of a collaborator',
				action: 'Get username from email or name',
			},
		],
		default: 'snapshot',
	},
	...snapshot.description,
	...metadata.description,
	...collaborator.description,
];
