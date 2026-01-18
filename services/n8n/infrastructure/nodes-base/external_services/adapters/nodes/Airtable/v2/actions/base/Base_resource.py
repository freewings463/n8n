"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtable/v2/actions/base/Base.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtable/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./getMany.operation、./getSchema.operation。导出:getMany、getSchema、description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtable/v2/actions/base/Base.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtable/v2/actions/base/Base_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as getMany from './getMany.operation';
import * as getSchema from './getSchema.operation';

export { getMany, getSchema };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Get Many',
				value: 'getMany',
				description: 'List all the bases',
				action: 'Get many bases',
			},
			{
				name: 'Get Schema',
				value: 'getSchema',
				description: 'Get the schema of the tables in a base',
				action: 'Get base schema',
			},
		],
		default: 'getMany',
		displayOptions: {
			show: {
				resource: ['base'],
			},
		},
	},
	...getMany.description,
	...getSchema.description,
];
