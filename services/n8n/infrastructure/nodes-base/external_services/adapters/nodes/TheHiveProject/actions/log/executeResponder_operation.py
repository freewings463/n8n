"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/log/executeResponder.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的节点。导入/依赖:外部:@utils/utilities；内部:无；本地:../../descriptions、../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/log/executeResponder.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/log/executeResponder_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { updateDisplayOptions, wrapData } from '@utils/utilities';

import { logRLC, responderOptions } from '../../descriptions';
import { theHiveApiRequest } from '../../transport';

const properties: INodeProperties[] = [{ ...logRLC, name: 'id' }, responderOptions];

const displayOptions = {
	show: {
		resource: ['log'],
		operation: ['executeResponder'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	let responseData: IDataObject | IDataObject[] = [];

	const logId = this.getNodeParameter('id', i);
	const responderId = this.getNodeParameter('responder', i) as string;
	let body: IDataObject;
	let response;
	const qs: IDataObject = {};
	body = {
		responderId,
		objectId: logId,
		objectType: 'case_task_log',
	};
	response = await theHiveApiRequest.call(this, 'POST', '/connector/cortex/action' as string, body);
	body = {
		query: [
			{
				_name: 'listAction',
			},
			{
				_name: 'filter',
				_and: [
					{
						_field: 'cortexId',
						_value: response.cortexId,
					},
					{
						_field: 'objectId',
						_value: response.objectId,
					},
					{
						_field: 'startDate',
						_value: response.startDate,
					},
				],
			},
		],
	};
	qs.name = 'log-actions';
	do {
		response = await theHiveApiRequest.call(this, 'POST', '/v1/query', body, qs);
	} while (response.status === 'Waiting' || response.status === 'InProgress');

	responseData = response;

	const executionData = this.helpers.constructExecutionMetaData(wrapData(responseData), {
		itemData: { item: i },
	});

	return executionData;
}
