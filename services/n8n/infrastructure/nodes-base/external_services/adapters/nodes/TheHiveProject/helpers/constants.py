"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/helpers/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/helpers 的节点。导入/依赖:外部:无；内部:无；本地:./interfaces。导出:alertCommonFields、caseCommonFields、taskCommonFields、observableCommonFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/helpers/constants.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/helpers/constants.py

import { TLPs } from './interfaces';

export const alertCommonFields = [
	{
		displayName: 'Title',
		id: 'title',
		type: 'string',
		removed: false,
	},
	{
		displayName: 'Description',
		id: 'description',
		type: 'string',
		removed: false,
	},
	{
		displayName: 'Type',
		id: 'type',
		type: 'string',
		removed: false,
	},
	{
		displayName: 'Source',
		id: 'source',
		type: 'string',
		removed: false,
	},
	{
		displayName: 'Source Reference',
		id: 'sourceRef',
		type: 'string',
		removed: false,
	},
	{
		displayName: 'External Link',
		id: 'externalLink',
		type: 'string',
		removed: true,
	},
	{
		displayName: 'Severity (Severity of information)',
		id: 'severity',
		type: 'options',
		options: [
			{
				name: 'Low',
				value: 1,
			},
			{
				name: 'Medium',
				value: 2,
			},
			{
				name: 'High',
				value: 3,
			},
			{
				name: 'Critical',
				value: 4,
			},
		],
		removed: true,
	},
	{
		displayName: 'Date',
		id: 'date',
		type: 'dateTime',
		removed: true,
	},
	{
		displayName: 'Last Sync Date',
		id: 'lastSyncDate',
		type: 'dateTime',
		removed: true,
	},
	{
		displayName: 'Tags',
		id: 'tags',
		type: 'string',
		removed: true,
	},
	{
		displayName: 'Follow',
		id: 'follow',
		type: 'boolean',
		removed: true,
	},
	{
		displayName: 'Flag',
		id: 'flag',
		type: 'boolean',
		removed: true,
	},
	{
		displayName: 'TLP (Confidentiality of information)',
		id: 'tlp',
		type: 'options',
		options: [
			{
				name: 'White',
				value: TLPs.white,
			},
			{
				name: 'Green',
				value: TLPs.green,
			},
			{
				name: 'Amber',
				value: TLPs.amber,
			},
			{
				name: 'Red',
				value: TLPs.red,
			},
		],
		removed: true,
	},
	{
		displayName: 'PAP (Level of exposure of information)',
		id: 'pap',
		type: 'options',
		options: [
			{
				name: 'White',
				value: TLPs.white,
			},
			{
				name: 'Green',
				value: TLPs.green,
			},
			{
				name: 'Amber',
				value: TLPs.amber,
			},
			{
				name: 'Red',
				value: TLPs.red,
			},
		],
		removed: true,
	},
	{
		displayName: 'Summary',
		id: 'summary',
		type: 'string',
		removed: true,
	},
	{
		displayName: 'Status',
		id: 'status',
		type: 'options',
		removed: true,
	},
	{
		displayName: 'Case Template',
		id: 'caseTemplate',
		type: 'options',
		removed: true,
	},
	{
		displayName: 'Add Tags',
		id: 'addTags',
		type: 'string',
		canBeUsedToMatch: false,
		removed: true,
	},
	{
		displayName: 'Remove Tags',
		id: 'removeTags',
		type: 'string',
		canBeUsedToMatch: false,
		removed: true,
	},
];

export const caseCommonFields = [
	{
		displayName: 'Title',
		id: 'title',
		type: 'string',
		removed: false,
	},
	{
		displayName: 'Description',
		id: 'description',
		type: 'string',
		removed: false,
	},
	{
		displayName: 'Severity (Severity of information)',
		id: 'severity',
		type: 'options',
		options: [
			{
				name: 'Low',
				value: 1,
			},
			{
				name: 'Medium',
				value: 2,
			},
			{
				name: 'High',
				value: 3,
			},
			{
				name: 'Critical',
				value: 4,
			},
		],
		removed: false,
	},
	{
		displayName: 'Start Date',
		id: 'startDate',
		type: 'dateTime',
		removed: false,
	},
	{
		displayName: 'End Date',
		id: 'endDate',
		type: 'dateTime',
		removed: true,
	},
	{
		displayName: 'Tags',
		id: 'tags',
		type: 'string',
		removed: false,
	},
	{
		displayName: 'Flag',
		id: 'flag',
		type: 'boolean',
		removed: true,
	},
	{
		displayName: 'TLP (Confidentiality of information)',
		id: 'tlp',
		type: 'options',
		options: [
			{
				name: 'White',
				value: TLPs.white,
			},
			{
				name: 'Green',
				value: TLPs.green,
			},
			{
				name: 'Amber',
				value: TLPs.amber,
			},
			{
				name: 'Red',
				value: TLPs.red,
			},
		],
		removed: false,
	},
	{
		displayName: 'PAP (Level of exposure of information)',
		id: 'pap',
		type: 'options',
		options: [
			{
				name: 'White',
				value: TLPs.white,
			},
			{
				name: 'Green',
				value: TLPs.green,
			},
			{
				name: 'Amber',
				value: TLPs.amber,
			},
			{
				name: 'Red',
				value: TLPs.red,
			},
		],
		removed: false,
	},
	{
		displayName: 'Summary',
		id: 'summary',
		type: 'string',
		removed: true,
	},
	{
		displayName: 'Status',
		id: 'status',
		type: 'options',
		removed: true,
	},
	{
		displayName: 'Assignee',
		id: 'assignee',
		type: 'options',
		removed: true,
	},
	{
		displayName: 'Case Template',
		id: 'caseTemplate',
		type: 'options',
		removed: true,
	},
	{
		displayName: 'Tasks',
		id: 'tasks',
		type: 'array',
		removed: true,
	},
	{
		displayName: 'Sharing Parameters',
		id: 'sharingParameters',
		type: 'array',
		removed: true,
	},
	{
		displayName: 'Impact Status',
		id: 'impactStatus',
		type: 'string',
		removed: true,
	},
	{
		displayName: 'Task Rule',
		id: 'taskRule',
		type: 'string',
		removed: true,
	},
	{
		displayName: 'Observable Rule',
		id: 'observableRule',
		type: 'string',
		removed: true,
	},
	{
		displayName: 'Add Tags',
		id: 'addTags',
		type: 'string',
		removed: true,
	},
	{
		displayName: 'Remove Tags',
		id: 'removeTags',
		type: 'string',
		removed: true,
	},
];

export const taskCommonFields = [
	{
		displayName: 'Title',
		id: 'title',
		type: 'string',
		removed: false,
	},
	{
		displayName: 'Description',
		id: 'description',
		type: 'string',
		removed: false,
	},
	{
		displayName: 'Group',
		id: 'group',
		type: 'string',
		removed: false,
	},
	{
		displayName: 'Status',
		id: 'status',
		type: 'stirng',
		removed: true,
	},
	{
		displayName: 'Flag',
		id: 'flag',
		type: 'boolean',
		removed: false,
	},
	{
		displayName: 'Start Date',
		id: 'startDate',
		type: 'dateTime',
		removed: true,
	},
	{
		displayName: 'Due Date',
		id: 'dueDate',
		type: 'dateTime',
		removed: false,
	},
	{
		displayName: 'End Date',
		id: 'endDate',
		type: 'dateTime',
		removed: true,
	},
	{
		displayName: 'Assignee',
		id: 'assignee',
		type: 'options',
		removed: false,
	},
	{
		displayName: 'Mandatory',
		id: 'mandatory',
		type: 'boolean',
		removed: false,
	},
	{
		displayName: 'Order',
		id: 'order',
		type: 'number',
		removed: true,
	},
];

export const observableCommonFields = [
	{
		displayName: 'Data Type',
		id: 'dataType',
		type: 'options',
		removed: false,
	},
	{
		displayName: 'Start Date',
		id: 'startDate',
		type: 'dateTime',
		removed: true,
	},
	{
		displayName: 'Description',
		id: 'message',
		type: 'string',
		removed: false,
	},
	{
		displayName: 'Tags',
		id: 'tags',
		type: 'string',
		removed: false,
	},
	{
		displayName: 'TLP (Confidentiality of information)',
		id: 'tlp',
		type: 'options',
		options: [
			{
				name: 'White',
				value: TLPs.white,
			},
			{
				name: 'Green',
				value: TLPs.green,
			},
			{
				name: 'Amber',
				value: TLPs.amber,
			},
			{
				name: 'Red',
				value: TLPs.red,
			},
		],
		removed: false,
	},
	{
		displayName: 'PAP (Level of exposure of information)',
		id: 'pap',
		type: 'options',
		options: [
			{
				name: 'White',
				value: TLPs.white,
			},
			{
				name: 'Green',
				value: TLPs.green,
			},
			{
				name: 'Amber',
				value: TLPs.amber,
			},
			{
				name: 'Red',
				value: TLPs.red,
			},
		],
		removed: false,
	},
	{
		displayName: 'IOC',
		id: 'ioc',
		type: 'boolean',
		removed: false,
	},
	{
		displayName: 'Sighted',
		id: 'sighted',
		type: 'boolean',
		removed: false,
	},
	{
		displayName: 'Sighted At',
		id: 'sightedAt',
		type: 'dateTime',
		removed: true,
	},
	{
		displayName: 'Ignore Similarity',
		id: 'ignoreSimilarity',
		type: 'boolean',
		removed: false,
	},
	{
		displayName: 'Is Zip',
		id: 'isZip',
		type: 'boolean',
		removed: true,
	},
	{
		displayName: 'Zip Password',
		id: 'zipPassword',
		type: 'string',
		removed: true,
	},
	{
		displayName: 'Add Tags',
		id: 'addTags',
		type: 'string',
		removed: true,
	},
	{
		displayName: 'Remove Tags',
		id: 'removeTags',
		type: 'string',
		removed: true,
	},
];
