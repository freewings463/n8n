"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/task/create.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Teams 的节点。导入/依赖:外部:luxon、@utils/utilities；内部:n8n-workflow；本地:../../descriptions、../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/task/create.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Teams/v2/actions/task/create_operation.py

import { DateTime } from 'luxon';
import type { INodeProperties, IExecuteFunctions, IDataObject } from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import { bucketRLC, groupRLC, memberRLC, planRLC } from '../../descriptions';
import { microsoftApiRequest } from '../../transport';

const properties: INodeProperties[] = [
	groupRLC,
	planRLC,
	bucketRLC,
	{
		displayName: 'Title',
		name: 'title',
		required: true,
		type: 'string',
		default: '',
		placeholder: 'e.g. new task',
		description: 'Title of the task',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		default: {},
		placeholder: 'Add option',
		options: [
			{
				...memberRLC,
				displayName: 'Assigned To',
				name: 'assignedTo',
				description: 'Who the task should be assigned to',
				typeOptions: {
					loadOptionsDependsOn: ['groupId.balue'],
				},
			},
			{
				displayName: 'Due Date Time',
				name: 'dueDateTime',
				type: 'string',
				validateType: 'dateTime',
				default: '',
				description:
					'Date and time at which the task is due. The Timestamp type represents date and time information using ISO 8601 format and is always in UTC time.',
			},
			{
				displayName: 'Percent Complete',
				name: 'percentComplete',
				type: 'number',
				typeOptions: {
					minValue: 0,
					maxValue: 100,
				},
				default: 0,
				placeholder: 'e.g. 75',
				description:
					'Percentage of task completion. When set to 100, the task is considered completed.',
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['task'],
		operation: ['create'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number) {
	//https://docs.microsoft.com/en-us/graph/api/planner-post-tasks?view=graph-rest-1.0&tabs=http

	const planId = this.getNodeParameter('planId', i, '', { extractValue: true }) as string;
	const bucketId = this.getNodeParameter('bucketId', i, '', { extractValue: true }) as string;

	const title = this.getNodeParameter('title', i) as string;
	const options = this.getNodeParameter('options', i);

	const body: IDataObject = {
		planId,
		bucketId,
		title,
	};

	if (options.assignedTo) {
		options.assignedTo = this.getNodeParameter('options.assignedTo', i, '', {
			extractValue: true,
		}) as string;
	}

	if (options.dueDateTime && options.dueDateTime instanceof DateTime) {
		options.dueDateTime = options.dueDateTime.toISO();
	}

	Object.assign(body, options);

	if (body.assignedTo) {
		body.assignments = {
			[body.assignedTo as string]: {
				'@odata.type': 'microsoft.graph.plannerAssignment',
				orderHint: ' !',
			},
		};
		delete body.assignedTo;
	}

	return await microsoftApiRequest.call(this, 'POST', '/v1.0/planner/tasks', body);
}
