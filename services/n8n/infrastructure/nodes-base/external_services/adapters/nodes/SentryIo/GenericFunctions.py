"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SentryIo/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SentryIo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:sentryIoApiRequest、getNext、hasMore、sentryApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SentryIo/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SentryIo/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
	IWebhookFunctions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function sentryIoApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	qs: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
): Promise<any> {
	const authentication = this.getNodeParameter('authentication', 0);

	const options = {
		headers: {},
		method,
		qs,
		body,
		uri: uri || `https://sentry.io${resource}`,
		json: true,
	} satisfies IRequestOptions;
	if (!Object.keys(body as IDataObject).length) {
		delete options.body;
	}

	if (Object.keys(option).length !== 0) {
		Object.assign(options, option);
	}

	if (options.qs.limit) {
		delete options.qs.limit;
	}

	let credentialName;

	try {
		if (authentication === 'oAuth2') {
			return await this.helpers.requestOAuth2.call(this, 'sentryIoOAuth2Api', options);
		}

		if (authentication === 'accessToken') {
			credentialName = 'sentryIoApi';
		} else {
			credentialName = 'sentryIoServerApi';
		}

		const credentials = await this.getCredentials(credentialName);

		if (credentials.url) {
			options.uri = `${credentials?.url}${resource}`;
		}

		options.headers = {
			Authorization: `Bearer ${credentials?.token}`,
		};

		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

function getNext(link: string) {
	if (link === undefined) {
		return;
	}
	const next = link.split(',')[1];
	if (next.includes('rel="next"')) {
		return next.split(';')[0].replace('<', '').replace('>', '').trim();
	}
}

function hasMore(link: string) {
	if (link === undefined) {
		return;
	}
	const next = link.split(',')[1];
	if (next.includes('rel="next"')) {
		return next.includes('results="true"');
	}
}

export async function sentryApiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	let link;

	let uri: string | undefined;

	do {
		responseData = await sentryIoApiRequest.call(this, method, resource, body, query, uri, {
			resolveWithFullResponse: true,
		});
		link = responseData.headers.link;
		uri = getNext(link as string);
		returnData.push.apply(returnData, responseData.body as IDataObject[]);
		const limit = query.limit as number | undefined;
		if (limit && limit >= returnData.length) {
			return;
		}
	} while (hasMore(link as string));

	return returnData;
}
