"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/BambooHr/v1/transport/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/BambooHr/v1 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:apiRequest。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/BambooHr/v1/transport/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/BambooHr/v1/transport/__init__.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	JsonObject,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

/**
 * Make an API request to Mattermost
 */
export async function apiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: 'GET' | 'POST' | 'PUT' | 'DELETE',
	endpoint: string,
	body: string[] | IDataObject = {},
	query: IDataObject = {},
	option: IDataObject = {},
) {
	const credentials = await this.getCredentials('bambooHrApi');

	//set-up credentials
	const apiKey = credentials.apiKey;
	const subdomain = credentials.subdomain;

	//set-up uri
	const uri = `https://api.bamboohr.com/api/gateway.php/${subdomain}/v1/${endpoint}`;

	const options: IRequestOptions = {
		method,
		body,
		qs: query,
		url: uri,
		auth: {
			username: apiKey as string,
			password: 'x',
		},
		json: true,
	};

	if (Object.keys(option).length) {
		Object.assign(options, option);
	}

	if (!Object.keys(body).length) {
		delete options.body;
	}

	if (!Object.keys(query).length) {
		delete options.qs;
	}

	try {
		return await this.helpers.request(options);
	} catch (error) {
		const description = error?.response?.headers['x-bamboohr-error-messsage'] || '';
		const message = error?.message || '';
		throw new NodeApiError(this.getNode(), error as JsonObject, { message, description });
	}
}
