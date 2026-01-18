"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Notion/shared/descriptions/Filters.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Notion/shared 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:filters。关键函数/方法:filters。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Notion/shared/descriptions/Filters.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Notion/shared/descriptions/Filters.py

export const filters = (conditions: any) => [
	{
		displayName: 'Property Name or ID',
		name: 'key',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getFilterProperties',
			loadOptionsDependsOn: ['datatabaseId'],
		},
		default: '',
		description:
			'The name of the property to filter by. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Type',
		name: 'type',
		type: 'hidden',
		default: '={{$parameter["&key"].split("|")[1]}}',
	},
	...conditions,
	{
		displayName: 'Title',
		name: 'titleValue',
		type: 'string',
		displayOptions: {
			show: {
				type: ['title'],
			},
			hide: {
				condition: ['is_empty', 'is_not_empty'],
			},
		},
		default: '',
	},
	{
		displayName: 'Text',
		name: 'richTextValue',
		type: 'string',
		displayOptions: {
			show: {
				type: ['rich_text'],
			},
			hide: {
				condition: ['is_empty', 'is_not_empty'],
			},
		},
		default: '',
	},
	{
		displayName: 'Phone Number',
		name: 'phoneNumberValue',
		type: 'string',
		displayOptions: {
			show: {
				type: ['phone_number'],
			},
			hide: {
				condition: ['is_empty', 'is_not_empty'],
			},
		},
		default: '',
		description: 'Phone number. No structure is enforced.',
	},
	{
		displayName: 'Option Name or ID',
		name: 'multiSelectValue',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getPropertySelectValues',
		},
		displayOptions: {
			show: {
				type: ['multi_select'],
			},
			hide: {
				condition: ['is_empty', 'is_not_empty'],
			},
		},
		default: [],
	},
	{
		displayName: 'Option Name or ID',
		name: 'selectValue',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getPropertySelectValues',
		},
		displayOptions: {
			show: {
				type: ['select'],
			},
			hide: {
				condition: ['is_empty', 'is_not_empty'],
			},
		},
		default: '',
	},
	{
		displayName: 'Status Name or ID',
		name: 'statusValue',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getPropertySelectValues',
		},
		displayOptions: {
			show: {
				type: ['status'],
			},
		},
		default: '',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
	},
	{
		displayName: 'Email',
		name: 'emailValue',
		type: 'string',
		displayOptions: {
			show: {
				type: ['email'],
			},
			hide: {
				condition: ['is_empty', 'is_not_empty'],
			},
		},
		default: '',
	},
	{
		displayName: 'URL',
		name: 'urlValue',
		type: 'string',
		displayOptions: {
			show: {
				type: ['url'],
			},
			hide: {
				condition: ['is_empty', 'is_not_empty'],
			},
		},
		default: '',
	},
	{
		displayName: 'User Name or ID',
		name: 'peopleValue',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getUsers',
		},
		displayOptions: {
			show: {
				type: ['people'],
			},
			hide: {
				condition: ['is_empty', 'is_not_empty'],
			},
		},
		default: '',
		description:
			'List of users. Multiples can be defined separated by comma. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'User Name or ID',
		name: 'createdByValue',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getUsers',
		},
		displayOptions: {
			show: {
				type: ['created_by'],
			},
			hide: {
				condition: ['is_empty', 'is_not_empty'],
			},
		},
		default: '',
		description:
			'List of users. Multiples can be defined separated by comma. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'User Name or ID',
		name: 'lastEditedByValue',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getUsers',
		},
		displayOptions: {
			show: {
				type: ['last_edited_by'],
			},
			hide: {
				condition: ['is_empty', 'is_not_empty'],
			},
		},
		default: '',
		description:
			'List of users. Multiples can be defined separated by comma. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Relation ID',
		name: 'relationValue',
		type: 'string',
		displayOptions: {
			show: {
				type: ['relation'],
			},
			hide: {
				condition: ['is_empty', 'is_not_empty'],
			},
		},
		default: '',
	},
	{
		displayName: 'Checked',
		name: 'checkboxValue',
		displayOptions: {
			show: {
				type: ['checkbox'],
			},
		},
		type: 'boolean',
		default: false,
		description:
			'Whether or not the checkbox is checked. <code>true</code> represents checked. <code>false</code> represents unchecked',
	},
	{
		displayName: 'Number',
		name: 'numberValue',
		displayOptions: {
			show: {
				type: ['number'],
			},
			hide: {
				condition: ['is_empty', 'is_not_empty'],
			},
		},
		type: 'number',
		default: 0,
		description: 'Number value',
	},
	{
		displayName: 'Date',
		name: 'date',
		displayOptions: {
			show: {
				type: ['date'],
			},
			hide: {
				condition: [
					'is_empty',
					'is_not_empty',
					'past_week',
					'past_month',
					'past_year',
					'next_week',
					'next_month',
					'next_year',
				],
			},
		},
		type: 'dateTime',
		default: '',
		description: 'An ISO 8601 format date, with optional time',
	},
	{
		displayName: 'Created Time',
		name: 'createdTimeValue',
		displayOptions: {
			show: {
				type: ['created_time'],
			},
			hide: {
				condition: [
					'is_empty',
					'is_not_empty',
					'past_week',
					'past_month',
					'past_year',
					'next_week',
					'next_month',
					'next_year',
				],
			},
		},
		type: 'dateTime',
		default: '',
		description: 'An ISO 8601 format date, with optional time',
	},
	{
		displayName: 'Last Edited Time',
		name: 'lastEditedTime',
		displayOptions: {
			show: {
				type: ['last_edited_time'],
			},
			hide: {
				condition: [
					'is_empty',
					'is_not_empty',
					'past_week',
					'past_month',
					'past_year',
					'next_week',
					'next_month',
					'next_year',
				],
			},
		},
		type: 'dateTime',
		default: '',
		description: 'An ISO 8601 format date, with optional time',
	},
	//formula types
	{
		displayName: 'Number',
		name: 'numberValue',
		displayOptions: {
			show: {
				type: ['formula'],
				returnType: ['number'],
			},
			hide: {
				condition: ['is_empty', 'is_not_empty'],
			},
		},
		type: 'number',
		default: 0,
		description: 'Number value',
	},
	{
		displayName: 'Text',
		name: 'textValue',
		type: 'string',
		displayOptions: {
			show: {
				type: ['formula'],
				returnType: ['text'],
			},
			hide: {
				condition: ['is_empty', 'is_not_empty'],
			},
		},
		default: '',
	},
	{
		displayName: 'Boolean',
		name: 'checkboxValue',
		displayOptions: {
			show: {
				type: ['formula'],
				returnType: ['checkbox'],
			},
		},
		type: 'boolean',
		default: false,
		description:
			'Whether or not the checkbox is checked. <code>true</code> represents checked. <code>false</code> represents unchecked',
	},
	{
		displayName: 'Date',
		name: 'dateValue',
		displayOptions: {
			show: {
				type: ['formula'],
				returnType: ['date'],
			},
			hide: {
				condition: [
					'is_empty',
					'is_not_empty',
					'past_week',
					'past_month',
					'past_year',
					'next_week',
					'next_month',
					'next_year',
				],
			},
		},
		type: 'dateTime',
		default: '',
		description: 'An ISO 8601 format date, with optional time',
	},
];
