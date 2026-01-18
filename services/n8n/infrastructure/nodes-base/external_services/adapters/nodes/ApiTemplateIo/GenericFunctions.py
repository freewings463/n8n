"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/ApiTemplateIo/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/ApiTemplateIo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:validateJSON。关键函数/方法:apiTemplateIoApiRequest、loadResource、validateJSON、downloadImage。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/ApiTemplateIo/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/ApiTemplateIo/GenericFunctions.py

import type {
	IExecuteFunctions,
	ILoadOptionsFunctions,
	JsonObject,
	IRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function apiTemplateIoApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	qs = {},
	body = {},
) {
	const options: IRequestOptions = {
		headers: {
			'user-agent': 'n8n',
			Accept: 'application/json',
		},
		uri: `https://api.apitemplate.io/v1${endpoint}`,
		method,
		qs,
		body,
		followRedirect: true,
		followAllRedirects: true,
		json: true,
	};

	if (!Object.keys(body).length) {
		delete options.body;
	}

	if (!Object.keys(qs).length) {
		delete options.qs;
	}

	try {
		const response = await this.helpers.requestWithAuthentication.call(
			this,
			'apiTemplateIoApi',
			options,
		);
		if (response.status === 'error') {
			throw new NodeApiError(this.getNode(), response.message as JsonObject);
		}
		return response;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function loadResource(this: ILoadOptionsFunctions, resource: 'image' | 'pdf') {
	const target = resource === 'image' ? ['JPEG', 'PNG'] : ['PDF'];
	const templates = await apiTemplateIoApiRequest.call(this, 'GET', '/list-templates');
	const filtered = templates.filter(({ format }: { format: 'PDF' | 'JPEG' | 'PNG' }) =>
		target.includes(format),
	);

	return filtered.map(({ format, name, id }: { format: string; name: string; id: string }) => ({
		name: `${name} (${format})`,
		value: id,
	}));
}

export function validateJSON(json: string | object | undefined): any {
	let result;
	if (typeof json === 'object') {
		return json;
	}
	try {
		result = JSON.parse(json!);
	} catch (exception) {
		result = undefined;
	}
	return result;
}

export async function downloadImage(this: IExecuteFunctions, url: string) {
	return await this.helpers.request({
		uri: url,
		method: 'GET',
		json: false,
		encoding: null,
	});
}
