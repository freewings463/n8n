"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/HighLevel/v1/HighLevelV1.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/HighLevel/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./description/ContactDescription、./description/OpportunityDescription、./description/TaskDescription。导出:HighLevelV1。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/HighLevel/v1/HighLevelV1.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/HighLevel/v1/HighLevelV1_node.py

import type {
	INodeProperties,
	INodeType,
	INodeTypeBaseDescription,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { contactFields, contactNotes, contactOperations } from './description/ContactDescription';
import { opportunityFields, opportunityOperations } from './description/OpportunityDescription';
import { taskFields, taskOperations } from './description/TaskDescription';
import {
	getPipelineStages,
	getTimezones,
	getUsers,
	highLevelApiPagination,
} from './GenericFunctions';

const resources: INodeProperties[] = [
	{
		displayName: 'Resource',
		name: 'resource',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Contact',
				value: 'contact',
			},
			{
				name: 'Opportunity',
				value: 'opportunity',
			},
			{
				name: 'Task',
				value: 'task',
			},
		],
		default: 'contact',
		required: true,
	},
];

const versionDescription: INodeTypeDescription = {
	displayName: 'HighLevel',
	name: 'highLevel',
	icon: 'file:highLevel.svg',
	group: ['transform'],
	version: 1,
	description: 'Consume HighLevel API v1',
	subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
	defaults: {
		name: 'HighLevel',
	},
	inputs: [NodeConnectionTypes.Main],
	outputs: [NodeConnectionTypes.Main],
	credentials: [
		{
			name: 'highLevelApi',
			required: true,
		},
	],
	requestDefaults: {
		baseURL: 'https://rest.gohighlevel.com/v1',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
	},
	requestOperations: {
		pagination: highLevelApiPagination,
	},
	properties: [
		...resources,
		...contactOperations,
		...contactNotes,
		...contactFields,
		...opportunityOperations,
		...opportunityFields,
		...taskOperations,
		...taskFields,
	],
};

export class HighLevelV1 implements INodeType {
	description: INodeTypeDescription;

	constructor(baseDescription: INodeTypeBaseDescription) {
		this.description = {
			...baseDescription,
			...versionDescription,
		};
	}

	methods = {
		loadOptions: {
			getPipelineStages,
			getUsers,
			getTimezones,
		},
	};
}
