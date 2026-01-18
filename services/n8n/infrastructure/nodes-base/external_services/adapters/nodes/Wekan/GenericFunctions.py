"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Wekan/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Wekan 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:apiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Wekan/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Wekan/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
} from 'n8n-workflow';

export async function apiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: object,
	query?: IDataObject,
): Promise<any> {
	const credentials = await this.getCredentials('wekanApi');

	query = query || {};

	const options: IRequestOptions = {
		headers: {
			Accept: 'application/json',
		},
		method,
		body,
		qs: query,
		uri: `${credentials.url}/api/${endpoint}`,
		json: true,
	};

	return await this.helpers.requestWithAuthentication.call(this, 'wekanApi', options);
}
