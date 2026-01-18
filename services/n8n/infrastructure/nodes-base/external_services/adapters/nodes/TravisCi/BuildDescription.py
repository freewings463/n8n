"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TravisCi/BuildDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TravisCi 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:buildOperations、buildFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TravisCi/BuildDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TravisCi/BuildDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const buildOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['build'],
			},
		},
		options: [
			{
				name: 'Cancel',
				value: 'cancel',
				description: 'Cancel a build',
				action: 'Cancel a build',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Get a build',
				action: 'Get a build',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many builds',
				action: 'Get many builds',
			},
			{
				name: 'Restart',
				value: 'restart',
				description: 'Restart a build',
				action: 'Restart a build',
			},
			{
				name: 'Trigger',
				value: 'trigger',
				description: 'Trigger a build',
				action: 'Trigger a build',
			},
		],
		default: 'cancel',
	},
];

export const buildFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                               build:cancel                                 */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Build ID',
		name: 'buildId',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['cancel'],
				resource: ['build'],
			},
		},
		default: '',
		description: 'Value uniquely identifying the build',
	},

	/* -------------------------------------------------------------------------- */
	/*                                 build:get                                  */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Build ID',
		name: 'buildId',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['build'],
			},
		},
		default: '',
		description: 'Value uniquely identifying the build',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['build'],
				operation: ['get'],
			},
		},
		options: [
			{
				displayName: 'Include',
				name: 'include',
				type: 'string',
				default: '',
				placeholder: 'build.commit',
				description: 'List of attributes to eager load',
			},
		],
	},

	/* -------------------------------------------------------------------------- */
	/*                                 build:getAll                               */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['build'],
			},
		},
		default: false,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['build'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 500,
		},
		default: 100,
		description: 'Max number of results to return',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['build'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Include',
				name: 'include',
				type: 'string',
				default: '',
				placeholder: 'build.commit',
				description: 'List of attributes to eager load',
			},
			{
				displayName: 'Order',
				name: 'order',
				type: 'options',
				options: [
					{
						name: 'ASC',
						value: 'asc',
					},
					{
						name: 'DESC',
						value: 'desc',
					},
				],
				default: 'asc',
				description: 'You may specify order to sort your response',
			},
			{
				displayName: 'Sort By',
				name: 'sortBy',
				type: 'options',
				options: [
					{
						name: 'Created At',
						value: 'created_at',
					},
					{
						name: 'Finished At',
						value: 'finished_at',
					},
					{
						name: 'ID',
						value: 'id',
					},
					{
						name: 'Number',
						value: 'number',
					},
					{
						name: 'Started At',
						value: 'started_at',
					},
				],
				default: 'number',
			},
		],
	},

	/* -------------------------------------------------------------------------- */
	/*                                 build:restart                              */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Build ID',
		name: 'buildId',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['restart'],
				resource: ['build'],
			},
		},
		default: '',
		description: 'Value uniquely identifying the build',
	},

	/* -------------------------------------------------------------------------- */
	/*                                 build:trigger                              */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Slug',
		name: 'slug',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['trigger'],
				resource: ['build'],
			},
		},
		placeholder: 'n8n-io/n8n',
		default: '',
		description: 'Same as {ownerName}/{repositoryName}',
	},
	{
		displayName: 'Branch',
		name: 'branch',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['trigger'],
				resource: ['build'],
			},
		},
		default: '',
		placeholder: 'master',
		description: 'Branch requested to be built',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['build'],
				operation: ['trigger'],
			},
		},
		options: [
			{
				displayName: 'Message',
				name: 'message',
				type: 'string',
				default: '',
				description: 'Travis-ci status message attached to the request',
			},
			{
				displayName: 'Merge Mode',
				name: 'mergeMode',
				type: 'options',
				options: [
					{
						name: 'Deep Merge',
						value: 'deep_merge',
					},
					{
						name: 'Deep Merge Append',
						value: 'deep_merge_append',
					},
					{
						name: 'Deep Merge Prepend',
						value: 'deep_merge_prepend',
					},
					{
						name: 'Merge',
						value: 'merge',
					},
					{
						name: 'Replace',
						value: 'replace',
					},
				],
				default: '',
			},
		],
	},
];
