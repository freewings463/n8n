"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/Ollama/transport/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/Ollama 的入口。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:apiRequest。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/Ollama/transport/index.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/Ollama/transport/__init__.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
} from 'n8n-workflow';

type RequestParameters = {
	headers?: IDataObject;
	body?: IDataObject | string;
	qs?: IDataObject;
	option?: IDataObject;
};

export async function apiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	parameters?: RequestParameters,
) {
	const { body, qs, option } = parameters ?? {};

	const credentials = await this.getCredentials<{
		apiKey?: string;
		baseUrl: string;
	}>('ollamaApi');
	const apiKey = credentials.apiKey;
	if (apiKey !== undefined && typeof apiKey !== 'string') {
		throw new Error('API key must be a string');
	}

	const url = new URL(endpoint, credentials.baseUrl).toString();

	const headers = parameters?.headers ?? {};
	if (apiKey) {
		headers.Authorization = `Bearer ${apiKey}`;
	}

	const options = {
		headers: {
			'Content-Type': 'application/json',
			...headers,
		},
		method,
		body,
		qs,
		url,
		json: true,
	};

	if (option && Object.keys(option).length !== 0) {
		Object.assign(options, option);
	}

	return await this.helpers.httpRequestWithAuthentication.call(this, 'ollamaApi', options);
}
