"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Postmark/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Postmark 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:convertTriggerObjectToStringArray、eventExists。关键函数/方法:postmarkApiRequest、convertTriggerObjectToStringArray、eventExists。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Postmark/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Postmark/GenericFunctions.py

import type {
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	IHookFunctions,
	IWebhookFunctions,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function postmarkApiRequest(
	this: IExecuteFunctions | IWebhookFunctions | IHookFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,

	body: any = {},
	option: IDataObject = {},
): Promise<any> {
	let options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json',
		},
		method,
		body,
		uri: 'https://api.postmarkapp.com' + endpoint,
		json: true,
	};
	if (Object.keys(body as IDataObject).length === 0) {
		delete options.body;
	}
	options = Object.assign({}, options, option);

	try {
		return await this.helpers.requestWithAuthentication.call(this, 'postmarkApi', options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export function convertTriggerObjectToStringArray(webhookObject: any): string[] {
	const triggers = webhookObject.Triggers;
	const webhookEvents: string[] = [];

	// Translate Webhook trigger settings to string array
	if (triggers.Open.Enabled) {
		webhookEvents.push('open');
	}
	if (triggers.Open.PostFirstOpenOnly) {
		webhookEvents.push('firstOpen');
	}
	if (triggers.Click.Enabled) {
		webhookEvents.push('click');
	}
	if (triggers.Delivery.Enabled) {
		webhookEvents.push('delivery');
	}
	if (triggers.Bounce.Enabled) {
		webhookEvents.push('bounce');
	}
	if (triggers.Bounce.IncludeContent) {
		webhookEvents.push('includeContent');
	}
	if (triggers.SpamComplaint.Enabled) {
		webhookEvents.push('spamComplaint');
	}
	if (triggers.SpamComplaint.IncludeContent) {
		if (!webhookEvents.includes('IncludeContent')) {
			webhookEvents.push('includeContent');
		}
	}
	if (triggers.SubscriptionChange.Enabled) {
		webhookEvents.push('subscriptionChange');
	}

	return webhookEvents;
}

export function eventExists(currentEvents: string[], webhookEvents: string[]) {
	for (const currentEvent of currentEvents) {
		if (!webhookEvents.includes(currentEvent)) {
			return false;
		}
	}
	return true;
}
