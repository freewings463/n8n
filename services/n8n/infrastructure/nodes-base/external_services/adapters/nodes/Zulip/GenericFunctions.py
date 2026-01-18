"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Zulip/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Zulip 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./MessageInterface、./StreamInterface、./UserInterface。导出:validateJSON。关键函数/方法:zulipApiRequest、validateJSON。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Zulip/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Zulip/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IHookFunctions,
	IWebhookFunctions,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

import type { IMessage } from './MessageInterface';
import type { IStream } from './StreamInterface';
import type { IUser } from './UserInterface';

export async function zulipApiRequest(
	this: IExecuteFunctions | IWebhookFunctions | IHookFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: IMessage | IStream | IUser = {},
	query: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
) {
	const credentials = await this.getCredentials('zulipApi');

	const endpoint = `${credentials.url.toString().replace(new RegExp('/$'), '')}/api/v1`;

	let options: IRequestOptions = {
		auth: {
			user: credentials.email as string,
			password: credentials.apiKey as string,
		},
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
		},
		method,
		form: body as IDataObject,
		qs: query,
		uri: uri || `${endpoint}${resource}`,
		json: true,
	};
	if (!Object.keys(body).length) {
		delete options.form;
	}
	if (!Object.keys(query).length) {
		delete options.qs;
	}
	options = Object.assign({}, options, option);
	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export function validateJSON(json: string | undefined): any {
	let result;
	try {
		result = JSON.parse(json!);
	} catch (exception) {
		result = undefined;
	}
	return result;
}
