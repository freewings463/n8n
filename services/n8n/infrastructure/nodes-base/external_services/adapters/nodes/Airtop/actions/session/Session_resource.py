"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/session/Session.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./create.operation、./save.operation、./terminate.operation、./waitForDownload.operation。导出:create、save、terminate、waitForDownload、description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/session/Session.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/session/Session_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as create from './create.operation';
import * as save from './save.operation';
import * as terminate from './terminate.operation';
import * as waitForDownload from './waitForDownload.operation';

export { create, save, terminate, waitForDownload };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['session'],
			},
		},
		options: [
			{
				name: 'Create Session',
				value: 'create',
				description: 'Create an Airtop browser session',
				action: 'Create a session',
			},
			{
				name: 'Save Profile on Termination',
				value: 'save',
				description:
					'Save in a profile changes made in your browsing session such as cookies and local storage',
				action: 'Save a profile on session termination',
			},
			{
				name: 'Terminate Session',
				value: 'terminate',
				description: 'Terminate a session',
				action: 'Terminate a session',
			},
			{
				name: 'Wait for Download',
				value: 'waitForDownload',
				description: 'Wait for a file download to become available',
				action: 'Wait for a download',
			},
		],
		default: 'create',
	},
	...create.description,
	...save.description,
	...terminate.description,
	...waitForDownload.description,
];
