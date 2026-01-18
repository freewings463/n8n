"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/messageAttachment/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./add.operation、./download.operation、./get.operation、./getAll.operation。导出:add、download、get、getAll、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/messageAttachment/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/v2/actions/messageAttachment/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as add from './add.operation';
import * as download from './download.operation';
import * as get from './get.operation';
import * as getAll from './getAll.operation';

export { add, download, get, getAll };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['messageAttachment'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				description: 'Add an attachment to a message',
				action: 'Add an attachment',
			},
			{
				name: 'Download',
				value: 'download',
				description: 'Download an attachment from a message',
				action: 'Download an attachment',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve information about an attachment of a message',
				action: 'Get an attachment',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Retrieve information about the attachments of a message',
				action: 'Get many attachments',
			},
		],
		default: 'add',
	},
	...add.description,
	...download.description,
	...get.description,
	...getAll.description,
];
