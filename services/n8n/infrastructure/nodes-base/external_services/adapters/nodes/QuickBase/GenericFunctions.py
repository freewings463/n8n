"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/QuickBase/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/QuickBase 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:quickbaseApiRequest、getFieldsObject、quickbaseApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/QuickBase/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/QuickBase/GenericFunctions.py

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
import { NodeApiError, NodeOperationError } from 'n8n-workflow';

export async function quickbaseApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions | IHookFunctions | IWebhookFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	qs: IDataObject = {},
	option: IDataObject = {},
): Promise<any> {
	const credentials = await this.getCredentials('quickbaseApi');

	if (!credentials.hostname) {
		throw new NodeOperationError(this.getNode(), 'Hostname must be defined');
	}

	if (!credentials.userToken) {
		throw new NodeOperationError(this.getNode(), 'User Token must be defined');
	}

	try {
		const options: IRequestOptions = {
			headers: {
				'QB-Realm-Hostname': credentials.hostname,
				'User-Agent': 'n8n',
				Authorization: `QB-USER-TOKEN ${credentials.userToken}`,
				'Content-Type': 'application/json',
			},
			method,
			body,
			qs,
			uri: `https://api.quickbase.com/v1${resource}`,
			json: true,
		};

		if (Object.keys(body as IDataObject).length === 0) {
			delete options.body;
		}

		if (Object.keys(qs).length === 0) {
			delete options.qs;
		}

		if (Object.keys(option).length !== 0) {
			Object.assign(options, option);
		}

		return await this.helpers?.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function getFieldsObject(
	this: IHookFunctions | ILoadOptionsFunctions | IExecuteFunctions,
	tableId: string,
): Promise<any> {
	const fieldsLabelKey: { [key: string]: number } = {};
	const fieldsIdKey: { [key: number]: string } = {};
	const data = await quickbaseApiRequest.call(this, 'GET', '/fields', {}, { tableId });
	for (const field of data) {
		fieldsLabelKey[field.label] = field.id;
		fieldsIdKey[field.id] = field.label;
	}
	return { fieldsLabelKey, fieldsIdKey };
}

export async function quickbaseApiRequestAllItems(
	this: IHookFunctions | ILoadOptionsFunctions | IExecuteFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData = [];

	if (method === 'POST') {
		body.options = {
			skip: 0,
			top: 100,
		};
	} else {
		query.skip = 0;
		query.top = 100;
	}

	let metadata;

	do {
		const {
			data,
			fields,
			metadata: meta,
		} = await quickbaseApiRequest.call(this, method, resource, body, query);

		metadata = meta;

		const fieldsIdKey: { [key: string]: string } = {};

		for (const field of fields) {
			fieldsIdKey[field.id] = field.label;
		}

		for (const record of data) {
			const recordData: IDataObject = {};
			for (const [key, value] of Object.entries(record as IDataObject)) {
				recordData[fieldsIdKey[key]] = (value as IDataObject).value;
			}
			responseData.push(recordData);
		}

		if (method === 'POST') {
			body.options.skip += body.options.top;
		} else {
			//@ts-ignore
			query.skip += query.top;
		}
		returnData.push.apply(returnData, responseData);
		responseData = [];
	} while (returnData.length < metadata.totalRecords);

	return returnData;
}
