"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/actions/employee/get/execute.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/BambooHr/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport。导出:无。关键函数/方法:get。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/actions/employee/get/execute.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/actions/employee/get/execute.py

import type { IExecuteFunctions, IDataObject, INodeExecutionData } from 'n8n-workflow';

import { apiRequest } from '../../../transport';

export async function get(this: IExecuteFunctions, index: number): Promise<INodeExecutionData[]> {
	const body: IDataObject = {};
	const requestMethod = 'GET';

	//meta data
	const id = this.getNodeParameter('employeeId', index) as string;

	//query parameters
	let fields = this.getNodeParameter('options.fields', index, ['all']) as string[];

	if (fields.includes('all')) {
		const { fields: allFields } = await apiRequest.call(
			this,
			requestMethod,
			'employees/directory',
			body,
		);
		fields = allFields.map((field: IDataObject) => field.id);
	}

	//endpoint
	const endpoint = `employees/${id}?fields=${fields}`;

	//response
	const responseData = await apiRequest.call(this, requestMethod, endpoint, body);

	//return
	return this.helpers.returnJsonArray(responseData as IDataObject[]);
}
