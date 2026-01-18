"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Segment/IdentifyDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Segment 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:identifyOperations、identifyFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Segment/IdentifyDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Segment/IdentifyDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const identifyOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['identify'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create an identity',
				action: 'Create an identity',
			},
		],
		default: 'create',
	},
];

export const identifyFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                identify:create                             */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'User ID',
		name: 'userId',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['identify'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Traits',
		name: 'traits',
		placeholder: 'Add Trait',
		type: 'fixedCollection',
		typeOptions: {
			multipleValues: true,
		},
		displayOptions: {
			show: {
				resource: ['identify'],
				operation: ['create'],
			},
		},
		default: {},
		options: [
			{
				name: 'traitsUi',
				displayName: 'Trait',
				values: [
					{
						displayName: 'Key',
						name: 'key',
						type: 'string',
						default: '',
					},
					{
						displayName: 'Value',
						name: 'value',
						type: 'string',
						default: '',
					},
				],
			},
		],
	},
	{
		displayName: 'Context',
		name: 'context',
		placeholder: 'Add Context',
		type: 'fixedCollection',
		typeOptions: {
			multipleValues: false,
		},
		displayOptions: {
			show: {
				resource: ['identify'],
				operation: ['create'],
			},
		},
		default: {},
		options: [
			{
				name: 'contextUi',
				displayName: 'Context',
				values: [
					{
						displayName: 'Active',
						name: 'active',
						type: 'boolean',
						default: false,
						description: 'Whether a user is active',
					},
					{
						displayName: 'IP',
						name: 'ip',
						type: 'string',
						default: '',
						description: 'Current user’s IP address',
					},
					{
						displayName: 'Locale',
						name: 'locate',
						type: 'string',
						default: '',
						description: 'Locale string for the current user, for example en-US',
					},
					{
						displayName: 'Page',
						name: 'page',
						type: 'string',
						default: '',
						description:
							'Dictionary of information about the current page in the browser, containing hash, path, referrer, search, title and URL',
					},
					{
						displayName: 'Timezone',
						name: 'timezone',
						type: 'string',
						default: '',
						description:
							'Timezones are sent as tzdata strings to add user timezone information which might be stripped from the timestamp, for example America/New_York',
					},
					{
						displayName: 'App',
						name: 'app',
						placeholder: 'Add App',
						type: 'fixedCollection',
						typeOptions: {
							multipleValues: false,
						},
						default: {},
						options: [
							{
								name: 'appUi',
								displayName: 'App',
								values: [
									{
										displayName: 'Name',
										name: 'name',
										type: 'string',
										default: '',
									},
									{
										displayName: 'Version',
										name: 'version',
										type: 'string',
										default: '',
									},
									{
										displayName: 'Build',
										name: 'build',
										type: 'string',
										default: '',
									},
								],
							},
						],
					},
					{
						displayName: 'Campaign',
						name: 'campaign',
						placeholder: 'Campaign App',
						type: 'fixedCollection',
						typeOptions: {
							multipleValues: false,
						},
						default: {},
						options: [
							{
								name: 'campaignUi',
								displayName: 'Campaign',
								values: [
									{
										displayName: 'Name',
										name: 'name',
										type: 'string',
										default: '',
									},
									{
										displayName: 'Source',
										name: 'source',
										type: 'string',
										default: '',
									},
									{
										displayName: 'Medium',
										name: 'medium',
										type: 'string',
										default: '',
									},
									{
										displayName: 'Term',
										name: 'term',
										type: 'string',
										default: '',
									},
									{
										displayName: 'Content',
										name: 'content',
										type: 'string',
										default: '',
									},
								],
							},
						],
					},
					{
						displayName: 'Device',
						name: 'device',
						placeholder: 'Add Device',
						type: 'fixedCollection',
						typeOptions: {
							multipleValues: false,
						},
						default: {},
						options: [
							{
								name: 'deviceUi',
								displayName: 'Device',
								values: [
									{
										displayName: 'ID',
										name: 'id',
										type: 'string',
										default: '',
									},
									{
										displayName: 'Manufacturer',
										name: 'manufacturer',
										type: 'string',
										default: '',
									},
									{
										displayName: 'Model',
										name: 'model',
										type: 'string',
										default: '',
									},
									{
										displayName: 'Name',
										name: 'name',
										type: 'string',
										default: '',
									},
									{
										displayName: 'Type',
										name: 'type',
										type: 'string',
										default: '',
									},
									{
										displayName: 'Version',
										name: 'version',
										type: 'string',
										default: '',
									},
								],
							},
						],
					},
				],
			},
		],
	},
	{
		displayName: 'Integration',
		name: 'integrations',
		placeholder: 'Add Integration',
		type: 'fixedCollection',
		typeOptions: {
			multipleValues: false,
		},
		displayOptions: {
			show: {
				resource: ['identify'],
				operation: ['create'],
			},
		},
		default: {},
		options: [
			{
				name: 'integrationsUi',
				displayName: 'Integration',
				values: [
					{
						displayName: 'All',
						name: 'all',
						type: 'boolean',
						default: true,
					},
					{
						displayName: 'Salesforce',
						name: 'salesforce',
						type: 'boolean',
						default: false,
					},
				],
			},
		],
	},
];
