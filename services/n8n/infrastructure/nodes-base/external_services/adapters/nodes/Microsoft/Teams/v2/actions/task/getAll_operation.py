"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/task/getAll.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Teams 的节点。导入/依赖:外部:@utils/descriptions、@utils/utilities；内部:n8n-workflow；本地:../../descriptions、../../transport。导出:description。关键函数/方法:execute、memberId。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/task/getAll.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Teams/v2/actions/task/getAll_operation.py

import type { INodeProperties, IExecuteFunctions } from 'n8n-workflow';

import { returnAllOrLimit } from '@utils/descriptions';
import { updateDisplayOptions } from '@utils/utilities';

import { groupRLC, planRLC } from '../../descriptions';
import { microsoftApiRequest, microsoftApiRequestAllItems } from '../../transport';

const properties: INodeProperties[] = [
	{
		displayName: 'Tasks For',
		name: 'tasksFor',
		default: 'member',
		required: true,
		type: 'options',
		description: 'Whether to retrieve the tasks for a user or for a plan',
		options: [
			{
				name: 'Group Member',
				value: 'member',
				description: 'Tasks assigned to group member',
			},
			{
				name: 'Plan',
				value: 'plan',
				description: 'Tasks in group plan',
			},
		],
	},
	groupRLC,
	{
		...planRLC,
		displayOptions: {
			show: {
				tasksFor: ['plan'],
			},
		},
	},
	...returnAllOrLimit,
];

const displayOptions = {
	show: {
		resource: ['task'],
		operation: ['getAll'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number) {
	const tasksFor = this.getNodeParameter('tasksFor', i) as string;
	const returnAll = this.getNodeParameter('returnAll', i);

	if (tasksFor === 'member') {
		//https://docs.microsoft.com/en-us/graph/api/planneruser-list-tasks?view=graph-rest-1.0&tabs=http
		const memberId = ((await microsoftApiRequest.call(this, 'GET', '/v1.0/me')) as { id: string })
			.id;
		if (returnAll) {
			return await microsoftApiRequestAllItems.call(
				this,
				'value',
				'GET',
				`/v1.0/users/${memberId}/planner/tasks`,
			);
		} else {
			const limit = this.getNodeParameter('limit', i);
			const responseData = await microsoftApiRequestAllItems.call(
				this,
				'value',
				'GET',
				`/v1.0/users/${memberId}/planner/tasks`,
				{},
			);
			return responseData.splice(0, limit);
		}
	} else {
		//https://docs.microsoft.com/en-us/graph/api/plannerplan-list-tasks?view=graph-rest-1.0&tabs=http
		const planId = this.getNodeParameter('planId', i, '', { extractValue: true }) as string;
		if (returnAll) {
			return await microsoftApiRequestAllItems.call(
				this,
				'value',
				'GET',
				`/v1.0/planner/plans/${planId}/tasks`,
			);
		} else {
			const limit = this.getNodeParameter('limit', i);
			const responseData = await microsoftApiRequestAllItems.call(
				this,
				'value',
				'GET',
				`/v1.0/planner/plans/${planId}/tasks`,
				{},
			);
			return responseData.splice(0, limit);
		}
	}
}
