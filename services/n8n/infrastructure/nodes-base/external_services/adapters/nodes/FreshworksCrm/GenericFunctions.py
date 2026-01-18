"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/FreshworksCrm/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/FreshworksCrm 的节点。导入/依赖:外部:lodash/omit；内部:n8n-workflow；本地:无。导出:adjustAttendees、adjustAccounts、throwOnEmptyUpdate、throwOnEmptyFilter。关键函数/方法:freshworksCrmApiRequest、getAllItemsViewId、response、freshworksCrmApiRequestAllItems、handleListing、loadResource、adjustAttendees、adjustAccounts、throwOnEmptyUpdate、throwOnEmptyFilter。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/FreshworksCrm/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/FreshworksCrm/GenericFunctions.py

import omit from 'lodash/omit';
import type {
	IExecuteFunctions,
	IDataObject,
	ILoadOptionsFunctions,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { NodeApiError, NodeOperationError } from 'n8n-workflow';

import type {
	FreshworksConfigResponse,
	FreshworksCrmApiCredentials,
	LoadedResource,
	SalesAccounts,
	ViewsResponse,
} from './types';

export async function freshworksCrmApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	qs: IDataObject = {},
) {
	const { domain } = await this.getCredentials<FreshworksCrmApiCredentials>('freshworksCrmApi');

	const options: IRequestOptions = {
		method,
		body,
		qs,
		uri: `https://${domain}.myfreshworks.com/crm/sales/api${endpoint}`,
		json: true,
	};

	if (!Object.keys(body).length) {
		delete options.body;
	}

	if (!Object.keys(qs).length) {
		delete options.qs;
	}
	try {
		const credentialsType = 'freshworksCrmApi';
		return await this.helpers.requestWithAuthentication.call(this, credentialsType, options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function getAllItemsViewId(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	{ fromLoadOptions } = { fromLoadOptions: false },
) {
	let resource = this.getNodeParameter('resource', 0);
	let keyword = 'All';

	if (resource === 'account' || fromLoadOptions) {
		resource = 'sales_account'; // adjust resource to endpoint
	}

	if (resource === 'deal') {
		keyword = 'My Deals'; // no 'All Deals' available
	}

	const response = (await freshworksCrmApiRequest.call(
		this,
		'GET',
		`/${resource}s/filters`,
	)) as ViewsResponse;

	const view = response.filters.find((v) => v.name.includes(keyword));

	if (!view) {
		throw new NodeOperationError(this.getNode(), 'Failed to get all items view');
	}

	return view.id.toString();
}

export async function freshworksCrmApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	qs: IDataObject = {},
) {
	const returnData: IDataObject[] = [];
	let response: any;

	qs.page = 1;

	do {
		response = await freshworksCrmApiRequest.call(this, method, endpoint, body, qs);
		const key = Object.keys(response as IDataObject)[0];
		returnData.push(...(response[key] as IDataObject[]));
		qs.page++;
	} while (response.meta.total_pages && qs.page <= response.meta.total_pages);

	return returnData;
}

export async function handleListing(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	qs: IDataObject = {},
) {
	const returnAll = this.getNodeParameter('returnAll', 0);

	if (returnAll) {
		return await freshworksCrmApiRequestAllItems.call(this, method, endpoint, body, qs);
	}

	const responseData = await freshworksCrmApiRequestAllItems.call(this, method, endpoint, body, qs);
	const limit = this.getNodeParameter('limit', 0) as number;

	if (limit) return responseData.slice(0, limit);

	return responseData;
}

/**
 * Load resources for options, except users.
 *
 * See: https://developers.freshworks.com/crm/api/#admin_configuration
 */
export async function loadResource(this: ILoadOptionsFunctions, resource: string) {
	const response = (await freshworksCrmApiRequest.call(
		this,
		'GET',
		`/selector/${resource}`,
	)) as FreshworksConfigResponse<LoadedResource>;

	const key = Object.keys(response)[0];
	return response[key].map(({ name, id }) => ({ name, value: id }));
}

export function adjustAttendees(attendees: [{ type: string; contactId: string; userId: string }]) {
	return attendees.map((attendee) => {
		if (attendee.type === 'contact') {
			return {
				attendee_type: 'Contact',
				attendee_id: attendee.contactId.toString(),
			};
		} else if (attendee.type === 'user') {
			return {
				attendee_type: 'FdMultitenant::User',
				attendee_id: attendee.userId.toString(),
			};
		}
	});
}

// /**
//  * Adjust attendee data from n8n UI to the format expected by Freshworks CRM API.
//  */
// export function adjustAttendees(additionalFields: IDataObject & Attendees) {
// 	if (!additionalFields?.appointment_attendees_attributes) return additionalFields;

// 	return {
// 		...omit(additionalFields, ['appointment_attendees_attributes']),
// 		appointment_attendees_attributes: additionalFields.appointment_attendees_attributes.map(attendeeId => {
// 			return { type: 'user', id: attendeeId };
// 		}),
// 	};
// }

/**
 * Adjust account data from n8n UI to the format expected by Freshworks CRM API.
 */
export function adjustAccounts(additionalFields: IDataObject & SalesAccounts) {
	if (!additionalFields?.sales_accounts) return additionalFields;

	const adjusted = additionalFields.sales_accounts.map((accountId) => {
		return { id: accountId, is_primary: false };
	});

	adjusted[0].is_primary = true;

	return {
		...omit(additionalFields, ['sales_accounts']),
		sales_accounts: adjusted,
	};
}

export function throwOnEmptyUpdate(this: IExecuteFunctions, resource: string) {
	throw new NodeOperationError(
		this.getNode(),
		`Please enter at least one field to update for the ${resource}.`,
	);
}

export function throwOnEmptyFilter(this: IExecuteFunctions) {
	throw new NodeOperationError(this.getNode(), 'Please select at least one filter.');
}
