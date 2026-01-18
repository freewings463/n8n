"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Formstack/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Formstack 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IFormstackFieldDefinitionType、IFormstackWebhookResponseBody、IFormstackSubmissionFieldContainer、FormstackFieldFormats、FormstackFieldFormat。关键函数/方法:apiRequest、apiRequestAllItems、getForms、getFields、getSubmission。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Formstack/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Formstack/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IWebhookFunctions,
	INodePropertyOptions,
	JsonObject,
	IHttpRequestMethods,
	IRequestOptions,
} from 'n8n-workflow';
import { ApplicationError, NodeApiError } from 'n8n-workflow';

export interface IFormstackFieldDefinitionType {
	id: string;
	label: string;
	description: string;
	name: string;
	type: string;
	options: unknown;
	required: string;
	uniq: string;
	hidden: string;
	readonly: string;
	colspan: string;
	label_position: string;
	num_columns: string;
	date_format: string;
	time_format: string;
}

export interface IFormstackWebhookResponseBody {
	FormID: string;
	UniqueID: string;
}

export interface IFormstackSubmissionFieldContainer {
	field: string;
	value: string;
}

export const FormstackFieldFormats = {
	ID: 'id',
	Label: 'label',
	Name: 'name',
} as const;

export type FormstackFieldFormat =
	(typeof FormstackFieldFormats)[keyof typeof FormstackFieldFormats];

/**
 * Make an API request to Formstack
 *
 */
export async function apiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	query: IDataObject = {},
): Promise<any> {
	const authenticationMethod = this.getNodeParameter('authentication', 0);

	const options: IRequestOptions = {
		headers: {},
		method,
		body,
		qs: query || {},
		uri: `https://www.formstack.com/api/v2/${endpoint}`,
		json: true,
	};

	if (!Object.keys(body).length) {
		delete options.body;
	}

	try {
		if (authenticationMethod === 'accessToken') {
			const credentials = await this.getCredentials<{ accessToken: string }>('formstackApi');

			options.headers!.Authorization = `Bearer ${credentials.accessToken}`;
			return await this.helpers.request(options);
		} else {
			return await this.helpers.requestOAuth2.call(this, 'formstackOAuth2Api', options);
		}
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

/**
 * Make an API request to paginated Formstack endpoint
 * and return all results
 *
 * @param {(IHookFunctions | IExecuteFunctions)} this
 */
export async function apiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IWebhookFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject,
	dataKey: string,
	query?: IDataObject,
): Promise<any> {
	if (query === undefined) {
		query = {};
	}

	query.per_page = 200;
	query.page = 0;

	const returnData = {
		items: [] as IDataObject[],
	};

	let responseData;

	do {
		query.page += 1;

		responseData = await apiRequest.call(this, method, endpoint, body, query);
		returnData.items.push.apply(returnData.items, responseData[dataKey] as IDataObject[]);
	} while (
		responseData.total !== undefined &&
		Math.ceil(responseData.total / query.per_page) > query.page
	);

	return returnData;
}

/**
 * Returns all the available forms
 *
 */
export async function getForms(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const endpoint = 'form.json';
	const responseData = await apiRequestAllItems.call(this, 'GET', endpoint, {}, 'forms', {
		folders: false,
	});

	if (responseData.items === undefined) {
		throw new ApplicationError('No data got returned', { level: 'warning' });
	}
	const returnData: INodePropertyOptions[] = [];
	for (const baseData of responseData.items) {
		returnData.push({
			name: baseData.name,
			value: baseData.id,
		});
	}
	return returnData;
}

/**
 * Returns all the fields of a form
 *
 */
export async function getFields(
	this: IWebhookFunctions,
	formID: string,
): Promise<Record<string, IFormstackFieldDefinitionType>> {
	const endpoint = `form/${formID}.json`;
	const responseData = await apiRequestAllItems.call(this, 'GET', endpoint, {}, 'fields');

	if (responseData.items === undefined) {
		throw new ApplicationError('No form fields meta data got returned', { level: 'warning' });
	}

	const fields = responseData.items as IFormstackFieldDefinitionType[];
	const fieldMap: Record<string, IFormstackFieldDefinitionType> = {};

	fields.forEach((field) => {
		fieldMap[field.id] = field;
	});

	return fieldMap;
}

/**
 * Returns all the fields of a form
 *
 */
export async function getSubmission(
	this: ILoadOptionsFunctions | IWebhookFunctions,
	uniqueId: string,
): Promise<IFormstackSubmissionFieldContainer[]> {
	const endpoint = `submission/${uniqueId}.json`;
	const responseData = await apiRequestAllItems.call(this, 'GET', endpoint, {}, 'data');

	if (responseData.items === undefined) {
		throw new ApplicationError('No form fields meta data got returned', { level: 'warning' });
	}

	return responseData.items as IFormstackSubmissionFieldContainer[];
}
