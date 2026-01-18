"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mandrill/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mandrill 的节点。导入/依赖:外部:lodash/map；内部:n8n-workflow；本地:无。导出:getToEmailArray、getGoogleAnalyticsDomainsArray、getTags、validateJSON。关键函数/方法:mandrillApiRequest、getToEmailArray、getGoogleAnalyticsDomainsArray、getTags、validateJSON。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mandrill/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mandrill/GenericFunctions.py

import map from 'lodash/map';
import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function mandrillApiRequest(
	this: IExecuteFunctions | IHookFunctions | ILoadOptionsFunctions,
	resource: string,
	method: IHttpRequestMethods,
	action: string,

	body: any = {},
	headers?: IDataObject,
): Promise<any> {
	const credentials = await this.getCredentials('mandrillApi');

	const data = Object.assign({}, body, { key: credentials.apiKey });

	const endpoint = 'mandrillapp.com/api/1.0';

	const options: IRequestOptions = {
		headers,
		method,
		uri: `https://${endpoint}${resource}${action}.json`,
		body: data,
		json: true,
	};

	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export function getToEmailArray(toEmail: string): any {
	let toEmailArray;
	if (toEmail.split(',').length > 0) {
		const array = toEmail.split(',');
		toEmailArray = map(array, (email) => {
			return {
				email,
				type: 'to',
			};
		});
	} else {
		toEmailArray = [
			{
				email: toEmail,
				type: 'to',
			},
		];
	}
	return toEmailArray;
}

export function getGoogleAnalyticsDomainsArray(s: string): string[] {
	let array: string[] = [];
	if (s.split(',').length > 0) {
		array = s.split(',');
	} else {
		array = [s];
	}
	return array;
}

export function getTags(s: string): any[] {
	let array = [];
	if (s.split(',').length > 0) {
		array = s.split(',');
	} else {
		array = [s];
	}
	return array;
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
