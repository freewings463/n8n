"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/session/terminate.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:无；本地:../../GenericFunctions、../../transport、../common/fields。导出:description。关键函数/方法:execute、validateAirtopApiResponse。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/session/terminate.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/session/terminate_operation.py

import {
	type IDataObject,
	type IExecuteFunctions,
	type INodeExecutionData,
	type INodeProperties,
} from 'n8n-workflow';

import { validateAirtopApiResponse, validateSessionId } from '../../GenericFunctions';
import { apiRequest } from '../../transport';
import { sessionIdField } from '../common/fields';

export const description: INodeProperties[] = [
	{
		...sessionIdField,
		displayOptions: {
			show: {
				resource: ['session'],
				operation: ['terminate'],
			},
		},
	},
];

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const sessionId = validateSessionId.call(this, index);
	const response = await apiRequest.call(this, 'DELETE', `/sessions/${sessionId}`);

	// validate response
	validateAirtopApiResponse(this.getNode(), response);

	return this.helpers.returnJsonArray({ success: true } as IDataObject);
}
