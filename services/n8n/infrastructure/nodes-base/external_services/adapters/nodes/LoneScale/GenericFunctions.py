"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/LoneScale/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/LoneScale 的节点。导入/依赖:外部:无；内部:无；本地:./constants。导出:无。关键函数/方法:lonescaleApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/LoneScale/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/LoneScale/GenericFunctions.py

import {
	ApplicationError,
	type IHttpRequestMethods,
	type IDataObject,
	type IExecuteFunctions,
	type IHookFunctions,
	type ILoadOptionsFunctions,
	type IWebhookFunctions,
	type IRequestOptions,
} from 'n8n-workflow';

import { BASE_URL } from './constants';

export async function lonescaleApiRequest(
	this: IExecuteFunctions | IWebhookFunctions | IHookFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: IDataObject = {},
	query: IDataObject = {},
	uri?: string,
) {
	const endpoint = `${BASE_URL}`;
	const credentials = await this.getCredentials('loneScaleApi');
	const options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
			'X-API-KEY': credentials?.apiKey,
		},
		method,
		body,
		qs: query,
		uri: uri || `${endpoint}${resource}`,
		json: true,
	};
	if (!Object.keys(body).length) {
		delete options.body;
	}
	if (!Object.keys(query).length) {
		delete options.qs;
	}

	try {
		return await this.helpers.requestWithAuthentication.call(this, 'loneScaleApi', options);
	} catch (error) {
		if (error.response) {
			const errorMessage =
				error.response.body.message || error.response.body.description || error.message;
			throw new ApplicationError(
				`Autopilot error response [${error.statusCode}]: ${errorMessage}`,
				{ level: 'warning' },
			);
		}
		throw error;
	}
}
