"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/WhatsApp/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/WhatsApp 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../sendAndWait/utils、../utils/utilities。导出:WHATSAPP_BASE_URL、createMessage。关键函数/方法:appAccessTokenRead、whatsappApiRequest、appWebhookSubscriptionList、response、appWebhookSubscriptionCreate、appWebhookSubscriptionDelete、createMessage。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/WhatsApp/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/WhatsApp/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	IHttpRequestOptions,
	ILoadOptionsFunctions,
	IWebhookFunctions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

import type {
	WhatsAppAppWebhookSubscriptionsResponse,
	WhatsAppAppWebhookSubscription,
} from './types';
import type { SendAndWaitConfig } from '../../utils/sendAndWait/utils';
import { createUtmCampaignLink } from '../../utils/utilities';
export const WHATSAPP_BASE_URL = 'https://graph.facebook.com/v13.0/';

async function appAccessTokenRead(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
): Promise<{ access_token: string }> {
	const credentials = await this.getCredentials('whatsAppTriggerApi');

	const options: IHttpRequestOptions = {
		headers: {
			'content-type': 'application/x-www-form-urlencoded',
		},
		method: 'POST',
		body: {
			client_id: credentials.clientId,
			client_secret: credentials.clientSecret,
			grant_type: 'client_credentials',
		},
		url: 'https://graph.facebook.com/v19.0/oauth/access_token',
		json: true,
	};
	try {
		return await this.helpers.httpRequest.call(this, options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

async function whatsappApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body?: { type: 'json'; payload: IDataObject } | { type: 'form'; payload: IDataObject },
	qs: IDataObject = {},
): Promise<any> {
	const tokenResponse = await appAccessTokenRead.call(this);
	const appAccessToken = tokenResponse.access_token;

	const options: IHttpRequestOptions = {
		headers: {
			accept: 'application/json',
			authorization: `Bearer ${appAccessToken}`,
		},
		method,
		qs,
		body: body?.payload,
		url: `https://graph.facebook.com/v19.0${resource}`,
		json: true,
	};

	try {
		return await this.helpers.httpRequest.call(this, options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function appWebhookSubscriptionList(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	appId: string,
): Promise<WhatsAppAppWebhookSubscription[]> {
	const response = (await whatsappApiRequest.call(
		this,
		'GET',
		`/${appId}/subscriptions`,
	)) as WhatsAppAppWebhookSubscriptionsResponse;
	return response.data;
}

export async function appWebhookSubscriptionCreate(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	appId: string,
	subscription: IDataObject,
) {
	return await whatsappApiRequest.call(this, 'POST', `/${appId}/subscriptions`, {
		type: 'form',
		payload: { ...subscription },
	});
}

export async function appWebhookSubscriptionDelete(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	appId: string,
	object: string,
) {
	return await whatsappApiRequest.call(this, 'DELETE', `/${appId}/subscriptions`, {
		type: 'form',
		payload: { object },
	});
}

export const createMessage = (
	sendAndWaitConfig: SendAndWaitConfig,
	phoneNumberId: string,
	recipientPhoneNumber: string,
	instanceId: string,
): IHttpRequestOptions => {
	const buttons = sendAndWaitConfig.options.map((option) => {
		return `*${option.label}:*\n_${option.url}_\n\n`;
	});

	let n8nAttribution: string = '';
	if (sendAndWaitConfig.appendAttribution) {
		const attributionText = 'This message was sent automatically with ';
		const link = createUtmCampaignLink('n8n-nodes-base.whatsapp', instanceId);
		n8nAttribution = `\n\n${attributionText}${link}`;
	}

	return {
		baseURL: WHATSAPP_BASE_URL,
		method: 'POST',
		url: `${phoneNumberId}/messages`,
		body: {
			messaging_product: 'whatsapp',
			text: {
				body: `${sendAndWaitConfig.message}\n\n${buttons.join('')}${n8nAttribution}`,
			},
			type: 'text',
			to: recipientPhoneNumber,
		},
	};
};
