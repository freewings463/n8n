"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/CustomerIo/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/CustomerIo 的节点。导入/依赖:外部:lodash/get；内部:无；本地:无。导出:eventExists、validateJSON。关键函数/方法:customerIoApiRequest、eventExists、validateJSON。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/CustomerIo/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/CustomerIo/GenericFunctions.py

import get from 'lodash/get';
import type {
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	IHttpRequestMethods,
	IHttpRequestOptions,
} from 'n8n-workflow';

export async function customerIoApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: object,
	baseApi?: string,
	_query?: IDataObject,
) {
	const credentials = await this.getCredentials('customerIoApi');
	const options: IHttpRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
		},
		method,
		body,
		url: '',
		json: true,
	};

	if (baseApi === 'tracking') {
		const region = credentials.region;
		options.url = `https://${region}/api/v1${endpoint}`;
	} else if (baseApi === 'api') {
		const region = credentials.region;
		// Special handling for EU region
		if (region === 'track-eu.customer.io') {
			options.url = `https://api-eu.customer.io/v1/api${endpoint}`;
		} else {
			options.url = `https://api.customer.io/v1/api${endpoint}`;
		}
	} else if (baseApi === 'beta') {
		options.url = `https://beta-api.customer.io/v1/api${endpoint}`;
	}

	return await this.helpers.requestWithAuthentication.call(this, 'customerIoApi', options);
}

export function eventExists(currentEvents: string[], webhookEvents: IDataObject) {
	for (const currentEvent of currentEvents) {
		if (get(webhookEvents, [currentEvent.split('.')[0], currentEvent.split('.')[1]]) !== true) {
			return false;
		}
	}
	return true;
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
