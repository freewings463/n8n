"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/transport/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/transport 的入口。导入/依赖:外部:无；内部:无；本地:./types、../constants。导出:无。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/transport/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/transport/__init__.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHttpRequestMethods,
	IHttpRequestOptions,
	ILoadOptionsFunctions,
} from 'n8n-workflow';

import type { IAirtopResponse } from './types';
import { BASE_URL, N8N_VERSION } from '../constants';

const defaultHeaders = {
	'Content-Type': 'application/json',
	'x-airtop-sdk-environment': 'n8n',
	'x-airtop-sdk-version': N8N_VERSION,
};

export async function apiRequest<T extends IAirtopResponse = IAirtopResponse>(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	query: IDataObject = {},
): Promise<T> {
	const options: IHttpRequestOptions = {
		headers: defaultHeaders,
		method,
		body,
		qs: query,
		url: endpoint.startsWith('http') ? endpoint : `${BASE_URL}${endpoint}`,
		json: true,
	};

	if (Object.keys(body).length === 0) {
		delete options.body;
	}

	return await this.helpers.httpRequestWithAuthentication.call<
		IExecuteFunctions | ILoadOptionsFunctions,
		[string, IHttpRequestOptions],
		Promise<T>
	>(this, 'airtopApi', options);
}
