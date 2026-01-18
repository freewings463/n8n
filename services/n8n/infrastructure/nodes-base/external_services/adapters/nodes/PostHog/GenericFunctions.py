"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/PostHog/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/PostHog 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IEvent、IAlias、ITrack、IIdentity。关键函数/方法:posthogApiRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/PostHog/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/PostHog/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function posthogApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	path: string,

	body: any = {},
	qs: IDataObject = {},
	_option = {},
): Promise<any> {
	const credentials = await this.getCredentials('postHogApi');

	const base = credentials.url as string;

	body.api_key = credentials.apiKey as string;

	const options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
		},
		method,
		body,
		qs,
		url: `${base}${path}`,
		json: true,
	};

	try {
		if (Object.keys(body as IDataObject).length === 0) {
			delete options.body;
		}
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export interface IEvent {
	event: string;
	properties: { [key: string]: any };
}

export interface IAlias {
	type: string;
	event: string;
	properties: { [key: string]: any };
	context: { [key: string]: any };
}

export interface ITrack {
	type: string;
	event: string;
	name: string;
	messageId?: string;
	distinct_id: string;
	category?: string;
	properties: { [key: string]: any };
	context: { [key: string]: any };
}

export interface IIdentity {
	event: string;
	messageId?: string;
	distinct_id: string;
	properties: { [key: string]: any };
}
