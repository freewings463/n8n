"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/task/update.operation.ts
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
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/task/update.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Teams/v2/actions/task/update_operation.py

import { DateTime } from 'luxon';
import type { INodeProperties, IExecuteFunctions, IDataObject } from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import { bucketRLC, groupRLC, memberRLC, planRLC } from '../../descriptions';
import { microsoftApiRequest } from '../../transport';

const properties: INodeProperties[] = [
	{
		displayName: 'Task ID',
		name: 'taskId',
		required: true,
		type: 'string',
		default: '',
		placeholder: 'e.g. h3ufgLvXPkSRzYm-zO5cY5gANtBQ',
		description: 'The ID of the task to update',
	},
	{
		displayName: 'Update Fields',
		name: 'updateFields',
		type: 'collection',
		default: {},
		placeholder: 'Add Field',
		options: [
			{
				...memberRLC,
				displayName: 'Assigned To',
				name: 'assignedTo',
				description: 'Who the task should be assigned to',
				hint: "Select 'Team' from options first",
				required: false,
				typeOptions: {
					loadOptionsDependsOn: ['updateFields.groupId.value'],
				},
			},
			{
				...bucketRLC,
				required: false,
				typeOptions: {
					loadOptionsDependsOn: ['updateFields.planId.value'],
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
				...groupRLC,
				required: false,
				typeOptions: {
					loadOptionsDependsOn: ['/groupSource'],
				},
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
			{
				...planRLC,
				required: false,
				hint: "Select 'Team' from options first",
				typeOptions: {
					loadOptionsDependsOn: ['updateFields.groupId.value'],
				},
			},
			{
				displayName: 'Title',
				name: 'title',
				type: 'string',
				default: '',
				placeholder: 'e.g. my task',
				description: 'Title of the task',
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['task'],
		operation: ['update'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number) {
	//https://docs.microsoft.com/en-us/graph/api/plannertask-update?view=graph-rest-1.0&tabs=http

	const taskId = this.getNodeParameter('taskId', i, '', { extractValue: true }) as string;
	const updateFields = this.getNodeParameter('updateFields', i);

	for (const key of Object.keys(updateFields)) {
		if (key === 'groupId') {
			// tasks are assigned to a plan and bucket, group is used for filtering
			delete updateFields.groupId;
			continue;
		}

		if (key === 'assignedTo') {
			const assignedTo = this.getNodeParameter('updateFields.assignedTo', i, '', {
				extractValue: true,
			}) as string;

			updateFields.assignments = {
				[assignedTo]: {
					'@odata.type': 'microsoft.graph.plannerAssignment',
					orderHint: ' !',
				},
			};
			delete updateFields.assignedTo;
			continue;
		}

		if (['bucketId', 'planId'].includes(key)) {
			updateFields[key] = this.getNodeParameter(`updateFields.${key}`, i, '', {
				extractValue: true,
			}) as string;
		}

		if (key === 'dueDateTime' && updateFields.dueDateTime instanceof DateTime) {
			updateFields.dueDateTime = updateFields.dueDateTime.toISO();
		}
	}

	const body: IDataObject = {};
	Object.assign(body, updateFields);

	const task = await microsoftApiRequest.call(this, 'GET', `/v1.0/planner/tasks/${taskId}`);

	await microsoftApiRequest.call(
		this,
		'PATCH',
		`/v1.0/planner/tasks/${taskId}`,
		body,
		{},
		undefined,
		{ 'If-Match': task['@odata.etag'] },
	);

	return { success: true };
}
