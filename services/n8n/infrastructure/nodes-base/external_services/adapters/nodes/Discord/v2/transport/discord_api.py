"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Discord/v2/transport/discord.api.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Discord/v2 的节点。导入/依赖:外部:form-data；内部:n8n-workflow；本地:./helpers。导出:无。关键函数/方法:discordApiRequest、discordApiMultiPartRequest。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Discord/v2/transport/discord.api.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Discord/v2/transport/discord_api.py

import type FormData from 'form-data';
import type {
	IDataObject,
	IExecuteFunctions,
	IExecuteSingleFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
} from 'n8n-workflow';
import { sleep, NodeApiError, jsonParse } from 'n8n-workflow';

import { getCredentialsType, requestApi } from './helpers';

export async function discordApiRequest(
	this: IHookFunctions | IExecuteFunctions | IExecuteSingleFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body?: IDataObject,
	qs?: IDataObject,
) {
	const authentication = this.getNodeParameter('authentication', 0, 'webhook') as string;
	const headers: IDataObject = {};

	const credentialType = getCredentialsType(authentication);

	const options: IRequestOptions = {
		headers,
		method,
		qs,
		body,
		url: `https://discord.com/api/v10${endpoint}`,
		json: true,
	};

	if (credentialType === 'discordWebhookApi') {
		const credentials = await this.getCredentials('discordWebhookApi');
		options.url = credentials.webhookUri as string;
	}

	try {
		const response = await requestApi.call(this, options, credentialType, endpoint);

		const resetAfter = Number(response.headers['x-ratelimit-reset-after']);
		const remaining = Number(response.headers['x-ratelimit-remaining']);

		if (remaining === 0) {
			await sleep(resetAfter);
		} else {
			await sleep(20); //prevent exceeding global rate limit of 50 requests per second
		}

		return response.body || { success: true };
	} catch (error) {
		throw new NodeApiError(this.getNode(), error);
	}
}

export async function discordApiMultiPartRequest(
	this: IHookFunctions | IExecuteFunctions | IExecuteSingleFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	formData: FormData,
) {
	const headers: IDataObject = {
		'content-type': 'multipart/form-data; charset=utf-8',
	};
	const authentication = this.getNodeParameter('authentication', 0, 'webhook') as string;

	const credentialType = getCredentialsType(authentication);

	const options: IRequestOptions = {
		headers,
		method,
		formData,
		url: `https://discord.com/api/v10${endpoint}`,
	};

	if (credentialType === 'discordWebhookApi') {
		const credentials = await this.getCredentials('discordWebhookApi');
		options.url = credentials.webhookUri as string;
	}

	try {
		const response = await requestApi.call(this, options, credentialType, endpoint);

		const resetAfter = Number(response.headers['x-ratelimit-reset-after']);
		const remaining = Number(response.headers['x-ratelimit-remaining']);

		if (remaining === 0) {
			await sleep(resetAfter);
		} else {
			await sleep(20); //prevent exceeding global rate limit of 50 requests per second
		}

		return jsonParse<IDataObject[]>(response.body);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error);
	}
}
