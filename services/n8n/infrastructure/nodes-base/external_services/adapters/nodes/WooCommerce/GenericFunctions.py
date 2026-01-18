"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/WooCommerce/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/WooCommerce 的节点。导入/依赖:外部:change-case、lodash/omit；内部:无；本地:./OrderInterface。导出:getAutomaticSecret、setMetadata、toSnakeCase、setFields、adjustMetadata。关键函数/方法:woocommerceApiRequest、woocommerceApiRequestAllItems、getAutomaticSecret、setMetadata、toSnakeCase、setFields、adjustMetadata。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/WooCommerce/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/WooCommerce/GenericFunctions.py

import { snakeCase } from 'change-case';
import { createHash } from 'crypto';
import omit from 'lodash/omit';
import type {
	ICredentialDataDecryptedObject,
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IWebhookFunctions,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';

import type { ICouponLine, IFeeLine, ILineItem, IShoppingLine } from './OrderInterface';

export async function woocommerceApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	qs: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
): Promise<any> {
	const credentials = await this.getCredentials('wooCommerceApi');

	let options: IRequestOptions = {
		method,
		qs,
		body,
		uri: uri || `${credentials.url}/wp-json/wc/v3${resource}`,
		json: true,
	};

	if (!Object.keys(body as IDataObject).length) {
		delete options.form;
	}
	options = Object.assign({}, options, option);
	return await this.helpers.requestWithAuthentication.call(this, 'wooCommerceApi', options);
}

export async function woocommerceApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions | IHookFunctions,
	method: IHttpRequestMethods,
	endpoint: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;
	let uri: string | undefined;
	query.per_page = 100;
	do {
		responseData = await woocommerceApiRequest.call(this, method, endpoint, body, query, uri, {
			resolveWithFullResponse: true,
		});
		const links = responseData.headers.link.split(',');
		const nextLink = links.find((link: string) => link.indexOf('rel="next"') !== -1);
		if (nextLink) {
			uri = nextLink.split(';')[0].replace(/<(.*)>/, '$1');
		}
		returnData.push.apply(returnData, responseData.body as IDataObject[]);
	} while (responseData.headers.link?.includes('rel="next"'));

	return returnData;
}

/**
 * Creates a secret from the credentials
 *
 */
export function getAutomaticSecret(credentials: ICredentialDataDecryptedObject) {
	const data = `${credentials.consumerKey},${credentials.consumerSecret}`;
	return createHash('md5').update(data).digest('hex');
}

export function setMetadata(data: IShoppingLine[] | IFeeLine[] | ILineItem[] | ICouponLine[]) {
	for (let i = 0; i < data.length; i++) {
		//@ts-ignore\
		if (data[i].metadataUi?.metadataValues) {
			//@ts-ignore
			data[i].meta_data = data[i].metadataUi.metadataValues;
			//@ts-ignore
			delete data[i].metadataUi;
		} else {
			//@ts-ignore
			delete data[i].metadataUi;
		}
	}
}

export function toSnakeCase(
	data: IShoppingLine[] | IFeeLine[] | ILineItem[] | ICouponLine[] | IDataObject,
) {
	if (!Array.isArray(data)) {
		data = [data];
	}
	let remove = false;
	for (let i = 0; i < data.length; i++) {
		for (const key of Object.keys(data[i])) {
			//@ts-ignore
			if (data[i][snakeCase(key)] === undefined) {
				remove = true;
			}
			//@ts-ignore
			data[i][snakeCase(key)] = data[i][key];
			if (remove) {
				//@ts-ignore
				delete data[i][key];
				remove = false;
			}
		}
	}
}

export function setFields(fieldsToSet: IDataObject, body: IDataObject) {
	for (const fields in fieldsToSet) {
		if (fields === 'tags') {
			body.tags = (fieldsToSet[fields] as string[]).map((tag) => ({ id: parseInt(tag, 10) }));
		} else {
			body[snakeCase(fields.toString())] = fieldsToSet[fields];
		}
	}
}

export function adjustMetadata(fields: IDataObject & Metadata) {
	if (!fields.meta_data) return fields;

	return {
		...omit(fields, ['meta_data']),
		meta_data: fields.meta_data.meta_data_fields,
	};
}

type Metadata = {
	meta_data?: {
		meta_data_fields: Array<{ key: string; value: string }>;
	};
};
