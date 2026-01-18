"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/task/get.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Teams 的节点。导入/依赖:外部:@utils/utilities；内部:n8n-workflow；本地:../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Teams/v2/actions/task/get.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Teams/v2/actions/task/get_operation.py

import type { INodeProperties, IExecuteFunctions } from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import { microsoftApiRequest } from '../../transport';

const properties: INodeProperties[] = [
	{
		displayName: 'Task ID',
		name: 'taskId',
		required: true,
		type: 'string',
		description: 'The ID of the task to retrieve',
		placeholder: 'e.g. h3ufgLvXPkSRzYm-zO5cY5gANtBQ',
		default: '',
	},
];

const displayOptions = {
	show: {
		resource: ['task'],
		operation: ['get'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number) {
	//https://docs.microsoft.com/en-us/graph/api/plannertask-get?view=graph-rest-1.0&tabs=http

	const taskId = this.getNodeParameter('taskId', i) as string;
	return await microsoftApiRequest.call(this, 'GET', `/v1.0/planner/tasks/${taskId}`);
}
