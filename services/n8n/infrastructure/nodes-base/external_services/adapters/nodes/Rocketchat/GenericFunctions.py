"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Rocketchat/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Rocketchat 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:validateJSON。关键函数/方法:rocketchatApiRequest、validateJSON。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Rocketchat/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Rocketchat/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
} from 'n8n-workflow';

export async function rocketchatApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	resource: string,
	method: IHttpRequestMethods,
	operation: string,

	body: any = {},
	headers?: IDataObject,
): Promise<any> {
	const credentials = await this.getCredentials('rocketchatApi');

	const options: IRequestOptions = {
		headers,
		method,
		body,
		uri: `${credentials.domain}/api/v1${resource}.${operation}`,
		json: true,
	};
	if (Object.keys(options.body as IDataObject).length === 0) {
		delete options.body;
	}
	return await this.helpers.requestWithAuthentication.call(this, 'rocketchatApi', options);
}

export function validateJSON(json: string | undefined): any {
	let result;
	try {
		result = JSON.parse(json!);
	} catch (exception) {
		result = [];
	}
	return result;
}
