"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Copper/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Copper 的节点。导入/依赖:外部:lodash/flow、lodash/omit；内部:n8n-workflow；本地:无。导出:getAutomaticSecret、adjustAddress、adjustPhoneNumbers、adjustEmails、adjustProjectIds、adjustEmail、adjustCompanyFields、adjustLeadFields 等2项。关键函数/方法:copperApiRequest、getAutomaticSecret、adjustAddress、adjustPhoneNumbers、adjustEmails、adjustProjectIds、adjustEmail 等2项。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Copper/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Copper/GenericFunctions.py

import { createHash } from 'crypto';
import flow from 'lodash/flow';
import omit from 'lodash/omit';
import type {
	ICredentialDataDecryptedObject,
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IHttpRequestOptions,
	IWebhookFunctions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

import type {
	AddressFixedCollection,
	EmailFixedCollection,
	EmailsFixedCollection,
	PhoneNumbersFixedCollection,
} from './utils/types';

/**
 * Make an authenticated API request to Copper.
 */
export async function copperApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: IDataObject = {},
	qs: IDataObject = {},
	uri = '',
	option: IDataObject = {},
) {
	let options: IHttpRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
		},
		method,
		qs,
		body,
		url: uri || `https://api.copper.com/developer_api/v1${resource}`,
		json: true,
	};

	options = Object.assign({}, options, option);

	if (!Object.keys(qs).length) {
		delete options.qs;
	}

	if (Object.keys(options.body as IDataObject).length === 0) {
		delete options.body;
	}

	try {
		return await this.helpers.requestWithAuthentication.call(this, 'copperApi', options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

/**
 * Creates a secret from the credentials
 *
 */
export function getAutomaticSecret(credentials: ICredentialDataDecryptedObject) {
	const data = `${credentials.email},${credentials.apiKey}`;
	return createHash('md5').update(data).digest('hex');
}

export function adjustAddress(fixedCollection: AddressFixedCollection) {
	if (!fixedCollection.address) return fixedCollection;

	const adjusted: { address?: object } = omit(fixedCollection, ['address']);

	if (fixedCollection.address) {
		adjusted.address = fixedCollection.address.addressFields;
	}

	return adjusted;
}

export function adjustPhoneNumbers(fixedCollection: PhoneNumbersFixedCollection) {
	if (!fixedCollection.phone_numbers) return fixedCollection;

	const adjusted: { phone_numbers?: object } = omit(fixedCollection, ['phone_numbers']);

	if (fixedCollection.phone_numbers) {
		adjusted.phone_numbers = fixedCollection.phone_numbers.phoneFields;
	}

	return adjusted;
}

export function adjustEmails(fixedCollection: EmailsFixedCollection) {
	if (!fixedCollection.emails) return fixedCollection;

	const adjusted: { emails?: object } = omit(fixedCollection, ['emails']);

	if (fixedCollection.emails) {
		adjusted.emails = fixedCollection.emails.emailFields;
	}

	return adjusted;
}

export function adjustProjectIds(fields: { project_ids?: string }) {
	if (!fields.project_ids) return fields;

	const adjusted: { project_ids?: string[] } = omit(fields, ['project_ids']);

	adjusted.project_ids = fields.project_ids.includes(',')
		? fields.project_ids.split(',')
		: [fields.project_ids];

	return adjusted;
}

export function adjustEmail(fixedCollection: EmailFixedCollection) {
	if (!fixedCollection.email) return fixedCollection;

	const adjusted: { email?: object } = omit(fixedCollection, ['email']);

	if (fixedCollection.email) {
		adjusted.email = fixedCollection.email.emailFields;
	}

	return adjusted;
}

export const adjustCompanyFields = flow(adjustAddress, adjustPhoneNumbers);
export const adjustLeadFields = flow(adjustCompanyFields, adjustEmail);
export const adjustPersonFields = flow(adjustCompanyFields, adjustEmails);
export const adjustTaskFields = flow(adjustLeadFields, adjustProjectIds);

/**
 * Make an authenticated API request to Copper and return all items.
 */
export async function copperApiRequestAllItems(
	this: IHookFunctions | ILoadOptionsFunctions | IExecuteFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: IDataObject = {},
	qs: IDataObject = {},
	uri = '',
	option: IDataObject = {},
) {
	let responseData;
	qs.page_size = 200;
	let totalItems = 0;
	const returnData: IDataObject[] = [];

	do {
		responseData = await copperApiRequest.call(this, method, resource, body, qs, uri, option);
		totalItems = responseData.headers['x-pw-total'];
		returnData.push(...(responseData.body as IDataObject[]));
	} while (totalItems > returnData.length);

	return returnData;
}

/**
 * Handle a Copper listing by returning all items or up to a limit.
 */
export async function handleListing(
	this: IExecuteFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	qs: IDataObject = {},
	body: IDataObject = {},
	uri = '',
) {
	const returnAll = this.getNodeParameter('returnAll', 0);

	const option = { resolveWithFullResponse: true };

	if (returnAll) {
		return await copperApiRequestAllItems.call(this, method, endpoint, body, qs, uri, option);
	}

	const limit = this.getNodeParameter('limit', 0);
	const responseData = await copperApiRequestAllItems.call(
		this,
		method,
		endpoint,
		body,
		qs,
		uri,
		option,
	);
	return responseData.slice(0, limit);
}
