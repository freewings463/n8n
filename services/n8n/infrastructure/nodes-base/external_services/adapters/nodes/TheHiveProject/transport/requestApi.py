"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/transport/requestApi.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/transport 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:theHiveApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/transport/requestApi.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/transport/requestApi.py

import type {
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	IHttpRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';

export async function theHiveApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: IDataObject | FormData = {},
	query: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
) {
	const credentials = await this.getCredentials('theHiveProjectApi');

	let options: IHttpRequestOptions = {
		method,
		qs: query,
		url: uri || `${credentials.url}/api${resource}`,
		body,
		skipSslCertificateValidation: credentials.allowUnauthorizedCerts as boolean,
		json: true,
	};

	if (Object.keys(option).length !== 0) {
		options = Object.assign({}, options, option);
	}

	if (Object.keys(body).length === 0) {
		delete options.body;
	}

	if (Object.keys(query).length === 0) {
		delete options.qs;
	}
	return await this.helpers.requestWithAuthentication.call(this, 'theHiveProjectApi', options);
}
