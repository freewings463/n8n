"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/transport/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/Anthropic 的入口。导入/依赖:外部:form-data；内部:无；本地:无。导出:无。关键函数/方法:apiRequest。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/transport/index.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/Anthropic/transport/__init__.py

import type FormData from 'form-data';
import type {
	IDataObject,
	IExecuteFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
} from 'n8n-workflow';

type RequestParameters = {
	headers?: IDataObject;
	body?: IDataObject | string | FormData;
	qs?: IDataObject;
	option?: IDataObject;
	enableAnthropicBetas?: {
		promptTools?: boolean;
		codeExecution?: boolean;
	};
};

export async function apiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	parameters?: RequestParameters,
) {
	const { body, qs, option, headers } = parameters ?? {};

	const credentials = await this.getCredentials('anthropicApi');
	const baseUrl = credentials.url ?? 'https://api.anthropic.com';
	const url = `${baseUrl}${endpoint}`;

	const betas = ['files-api-2025-04-14'];
	if (parameters?.enableAnthropicBetas?.promptTools) {
		betas.push('prompt-tools-2025-04-02');
	}

	if (parameters?.enableAnthropicBetas?.codeExecution) {
		betas.push('code-execution-2025-05-22');
	}

	const requestHeaders: IDataObject = {
		'anthropic-version': '2023-06-01',
		'anthropic-beta': betas.join(','),
		...headers,
	};

	if (
		credentials.header &&
		typeof credentials.headerName === 'string' &&
		credentials.headerName &&
		typeof credentials.headerValue === 'string'
	) {
		requestHeaders[credentials.headerName] = credentials.headerValue;
	}

	const options = {
		headers: requestHeaders,
		method,
		body,
		qs,
		url,
		json: true,
	};

	if (option && Object.keys(option).length !== 0) {
		Object.assign(options, option);
	}

	return await this.helpers.httpRequestWithAuthentication.call(this, 'anthropicApi', options);
}
