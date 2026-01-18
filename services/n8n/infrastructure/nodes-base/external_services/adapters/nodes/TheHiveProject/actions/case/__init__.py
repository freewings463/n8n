"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/case/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./addAttachment.operation、./create.operation、./deleteAttachment.operation、./deleteCase.operation 等6项。导出:description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/case/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/case/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as addAttachment from './addAttachment.operation';
import * as create from './create.operation';
import * as deleteAttachment from './deleteAttachment.operation';
import * as deleteCase from './deleteCase.operation';
import * as executeResponder from './executeResponder.operation';
import * as get from './get.operation';
import * as getAttachment from './getAttachment.operation';
import * as getTimeline from './getTimeline.operation';
import * as search from './search.operation';
import * as update from './update.operation';

export {
	addAttachment,
	create,
	deleteAttachment,
	deleteCase,
	executeResponder,
	get,
	search,
	getAttachment,
	getTimeline,
	update,
};

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		default: 'create',
		type: 'options',
		noDataExpression: true,
		required: true,
		options: [
			{
				name: 'Add Attachment',
				value: 'addAttachment',
				action: 'Add attachment to a case',
			},
			{
				name: 'Create',
				value: 'create',
				action: 'Create a case',
			},
			{
				name: 'Delete Attachment',
				value: 'deleteAttachment',
				action: 'Delete attachment from a case',
			},
			{
				name: 'Delete Case',
				value: 'deleteCase',
				action: 'Delete an case',
			},
			{
				name: 'Execute Responder',
				value: 'executeResponder',
				action: 'Execute responder on a case',
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get a case',
			},
			{
				name: 'Get Attachment',
				value: 'getAttachment',
				action: 'Get attachment from a case',
			},
			{
				name: 'Get Timeline',
				value: 'getTimeline',
				action: 'Get timeline of a case',
			},
			{
				name: 'Search',
				value: 'search',
				action: 'Search cases',
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a case',
			},
		],
		displayOptions: {
			show: {
				resource: ['case'],
			},
		},
	},
	...addAttachment.description,
	...create.description,
	...deleteAttachment.description,
	...deleteCase.description,
	...executeResponder.description,
	...get.description,
	...getAttachment.description,
	...search.description,
	...getTimeline.description,
	...update.description,
];
