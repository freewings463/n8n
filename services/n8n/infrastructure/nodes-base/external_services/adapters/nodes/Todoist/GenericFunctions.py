"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Todoist/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Todoist 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:Context、FormatDueDatetime。关键函数/方法:FormatDueDatetime、todoistApiRequest、todoistSyncRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Todoist/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Todoist/GenericFunctions.py

import type {
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export type Context = IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions;

export function FormatDueDatetime(isoString: string): string {
	// Assuming that the problem with incorrect date format was caused by milliseconds
	// Replacing the last 5 characters of ISO-formatted string with just Z char
	return isoString.replace(new RegExp('.000Z$'), 'Z');
}

export async function todoistApiRequest(
	this: Context,
	method: IHttpRequestMethods,
	resource: string,
	body: IDataObject = {},
	qs: IDataObject = {},
): Promise<any> {
	const authentication = this.getNodeParameter('authentication', 0) as string;

	const endpoint = 'api.todoist.com/rest/v2';

	const options: IRequestOptions = {
		method,
		qs,
		uri: `https://${endpoint}${resource}`,
		json: true,
	};

	if (Object.keys(body).length !== 0) {
		options.body = body;
	}

	try {
		const credentialType = authentication === 'apiKey' ? 'todoistApi' : 'todoistOAuth2Api';
		return await this.helpers.requestWithAuthentication.call(this, credentialType, options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function todoistSyncRequest(
	this: Context,
	body: any = {},
	qs: IDataObject = {},
	endpoint: string = '/sync',
): Promise<any> {
	const authentication = this.getNodeParameter('authentication', 0, 'oAuth2');

	const options: IRequestOptions = {
		headers: {},
		method: 'POST',
		qs,
		uri: `https://api.todoist.com/sync/v9${endpoint}`,
		json: true,
	};

	if (Object.keys(body as IDataObject).length !== 0) {
		options.body = body;
	}

	try {
		const credentialType = authentication === 'oAuth2' ? 'todoistOAuth2Api' : 'todoistApi';
		return await this.helpers.requestWithAuthentication.call(this, credentialType, options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}
