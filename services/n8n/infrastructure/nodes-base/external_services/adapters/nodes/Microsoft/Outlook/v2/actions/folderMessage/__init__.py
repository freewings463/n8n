"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/folderMessage/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./getAll.operation。导出:getAll、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/folderMessage/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/v2/actions/folderMessage/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as getAll from './getAll.operation';

export { getAll };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['folderMessage'],
			},
		},
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieves the messages in a folder',
				action: 'Get many folder messages',
			},
		],
		default: 'getAll',
	},

	...getAll.description,
];
