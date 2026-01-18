"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/draft/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./delete.operation、./get.operation、./send.operation 等1项。导出:create、del、get、send、update、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/draft/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/v2/actions/draft/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as del from './delete.operation';
import * as get from './get.operation';
import * as send from './send.operation';
import * as update from './update.operation';

export { create, del as delete, get, send, update };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['draft'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a new email draft',
				action: 'Create a draft',
			},
			{
				name: 'Delete',
				value: 'delete',
				description: 'Delete an email draft',
				action: 'Delete a draft',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve an email draft',
				action: 'Get a draft',
			},
			{
				name: 'Send',
				value: 'send',
				description: 'Send an existing email draft',
				action: 'Send a draft',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update an email draft',
				action: 'Update a draft',
			},
		],
		default: 'create',
	},

	...create.description,
	...del.description,
	...get.description,
	...send.description,
	...update.description,
];
