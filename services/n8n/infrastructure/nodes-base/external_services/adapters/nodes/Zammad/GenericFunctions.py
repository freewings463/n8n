"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Zammad/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Zammad 的节点。导入/依赖:外部:lodash/flow；内部:n8n-workflow；本地:./types。导出:tolerateTrailingSlash、throwOnEmptyUpdate、prettifyDisplayName、fieldToLoadOption、isCustomer、getGroupFields、getOrganizationFields、getUserFields 等7项。关键函数/方法:tolerateTrailingSlash、zammadApiRequest、zammadApiRequestAllItems、throwOnEmptyUpdate、prettifyDisplayName、fieldToLoadOption 等5项。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Zammad/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Zammad/GenericFunctions.py

import flow from 'lodash/flow';
import type {
	IExecuteFunctions,
	IDataObject,
	ILoadOptionsFunctions,
	JsonObject,
	IRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError, NodeOperationError } from 'n8n-workflow';

import type { Zammad } from './types';

export function tolerateTrailingSlash(url: string) {
	return url.endsWith('/') ? url.substr(0, url.length - 1) : url;
}

export async function zammadApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	qs: IDataObject = {},
) {
	const options: IRequestOptions = {
		method,
		body,
		qs,
		uri: '',
		json: true,
	};

	const authentication = this.getNodeParameter('authentication', 0) as 'basicAuth' | 'tokenAuth';

	if (authentication === 'basicAuth') {
		const credentials =
			await this.getCredentials<Zammad.BasicAuthCredentials>('zammadBasicAuthApi');

		const baseUrl = tolerateTrailingSlash(credentials.baseUrl);

		options.uri = `${baseUrl}/api/v1${endpoint}`;

		options.auth = {
			user: credentials.username,
			pass: credentials.password,
		};

		options.rejectUnauthorized = !credentials.allowUnauthorizedCerts;
	} else {
		const credentials =
			await this.getCredentials<Zammad.TokenAuthCredentials>('zammadTokenAuthApi');

		const baseUrl = tolerateTrailingSlash(credentials.baseUrl);

		options.uri = `${baseUrl}/api/v1${endpoint}`;

		options.headers = {
			Authorization: `Token token=${credentials.accessToken}`,
		};

		options.rejectUnauthorized = !credentials.allowUnauthorizedCerts;
	}

	if (!Object.keys(body).length) {
		delete options.body;
	}

	if (!Object.keys(qs).length) {
		delete options.qs;
	}

	try {
		return await this.helpers.request(options);
	} catch (error) {
		if (error.error.error === 'Object already exists!') {
			error.error.error = 'An entity with this name already exists.';
		}

		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function zammadApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	qs: IDataObject = {},
	limit = 0,
) {
	// https://docs.zammad.org/en/latest/api/intro.html#pagination

	const returnData: IDataObject[] = [];

	let responseData;
	qs.per_page = 20;
	qs.page = 1;

	do {
		responseData = await zammadApiRequest.call(this, method, endpoint, body, qs);
		returnData.push(...(responseData as IDataObject[]));

		if (limit && returnData.length > limit) {
			return returnData.slice(0, limit);
		}

		qs.page++;
	} while (responseData.length);

	return returnData;
}

export function throwOnEmptyUpdate(this: IExecuteFunctions, resource: string) {
	throw new NodeOperationError(
		this.getNode(),
		`Please enter at least one field to update for the ${resource}`,
	);
}

// ----------------------------------
//        loadOptions utils
// ----------------------------------

export const prettifyDisplayName = (fieldName: string) => fieldName.replace('name', ' Name');

export const fieldToLoadOption = (i: Zammad.Field) => {
	return { name: i.display ? prettifyDisplayName(i.display) : i.name, value: i.name };
};

export const isCustomer = (user: Zammad.User) =>
	user.role_ids.includes(3) && !user.email.endsWith('@zammad.org');

export async function getAllFields(this: ILoadOptionsFunctions) {
	return (await zammadApiRequest.call(this, 'GET', '/object_manager_attributes')) as Zammad.Field[];
}

const isTypeField =
	(resource: 'Group' | 'Organization' | 'Ticket' | 'User') => (arr: Zammad.Field[]) =>
		arr.filter((i) => i.object === resource);

export const getGroupFields = isTypeField('Group');
export const getOrganizationFields = isTypeField('Organization');
export const getUserFields = isTypeField('User');
export const getTicketFields = isTypeField('Ticket');

const getCustomFields = (arr: Zammad.Field[]) => arr.filter((i) => i.created_by_id !== 1);

export const getGroupCustomFields = flow(getGroupFields, getCustomFields);
export const getOrganizationCustomFields = flow(getOrganizationFields, getCustomFields);
export const getUserCustomFields = flow(getUserFields, getCustomFields);
export const getTicketCustomFields = flow(getTicketFields, getCustomFields);

export const isNotZammadFoundation = (i: Zammad.Organization) => i.name !== 'Zammad Foundation';

export const doesNotBelongToZammad = (i: Zammad.User) =>
	!i.email.endsWith('@zammad.org') && i.login !== '-';
