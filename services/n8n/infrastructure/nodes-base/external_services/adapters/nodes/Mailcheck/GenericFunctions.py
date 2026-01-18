"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Mailcheck/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Mailcheck 的节点。导入/依赖:外部:无；内部:@n8n/errors；本地:无。导出:无。关键函数/方法:mailCheckApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Mailcheck/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Mailcheck/GenericFunctions.py

import { ApplicationError } from '@n8n/errors';
import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
	IWebhookFunctions,
} from 'n8n-workflow';

export async function mailCheckApiRequest(
	this: IWebhookFunctions | IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	qs: IDataObject = {},
	uri?: string,
	headers: IDataObject = {},
	option: IDataObject = {},
): Promise<any> {
	const credentials = await this.getCredentials('mailcheckApi');

	let options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${credentials.apiKey}`,
		},
		method,
		body,
		qs,
		uri: uri || `https://api.mailcheck.co/v1${resource}`,
		json: true,
	};
	try {
		options = Object.assign({}, options, option);
		if (Object.keys(headers).length !== 0) {
			options.headers = Object.assign({}, options.headers, headers);
		}
		if (Object.keys(body as IDataObject).length === 0) {
			delete options.body;
		}
		return await this.helpers.request.call(this, options);
	} catch (error) {
		if (error.response?.body?.message) {
			// Try to return the error prettier
			throw new ApplicationError(
				`Mailcheck error response [${error.statusCode}]: ${error.response.body.message}`,
				{ level: 'warning' },
			);
		}
		throw error;
	}
}
