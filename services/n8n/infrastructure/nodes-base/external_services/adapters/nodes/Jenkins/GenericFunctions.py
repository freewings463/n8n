"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Jenkins/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Jenkins 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:tolerateTrailingSlash。关键函数/方法:tolerateTrailingSlash、jenkinsApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Jenkins/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Jenkins/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	JsonObject,
	IRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export function tolerateTrailingSlash(baseUrl: string) {
	return baseUrl.endsWith('/') ? baseUrl.substr(0, baseUrl.length - 1) : baseUrl;
}

export async function jenkinsApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	uri: string,
	qs: IDataObject = {},

	body: any = '',
	option: IDataObject = {},
): Promise<any> {
	const credentials = await this.getCredentials('jenkinsApi');
	let options: IRequestOptions = {
		headers: {
			Accept: 'application/json',
		},
		method,
		auth: {
			username: credentials.username as string,
			password: credentials.apiKey as string,
		},
		uri: `${tolerateTrailingSlash(credentials.baseUrl as string)}${uri}`,
		json: true,
		qs,
		body,
	};
	options = Object.assign({}, options, option);
	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}
