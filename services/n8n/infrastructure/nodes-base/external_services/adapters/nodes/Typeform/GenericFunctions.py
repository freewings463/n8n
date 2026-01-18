"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Typeform/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Typeform 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ITypeformDefinition、ITypeformDefinitionField、ITypeformAnswer、ITypeformAnswerField。关键函数/方法:apiRequest、apiRequestAllItems、getForms。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Typeform/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Typeform/GenericFunctions.py

import type {
	IExecuteFunctions,
	IHookFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	INodePropertyOptions,
	JsonObject,
	IRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError, NodeOperationError } from 'n8n-workflow';

// Interface in Typeform
export interface ITypeformDefinition {
	fields: ITypeformDefinitionField[];
}

export interface ITypeformDefinitionField {
	id: string;
	title: string;
}

export interface ITypeformAnswer {
	field: ITypeformAnswerField;
	type: string;
	[key: string]: string | ITypeformAnswerField | object;
}

export interface ITypeformAnswerField {
	id: string;
	type: string;
	ref: string;
	[key: string]: string | object;
}

/**
 * Make an API request to Typeform
 *
 */
export async function apiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: object,
	query?: IDataObject,
): Promise<any> {
	const authenticationMethod = this.getNodeParameter('authentication', 0);

	const options: IRequestOptions = {
		headers: {},
		method,
		body,
		qs: query,
		uri: `https://api.typeform.com/${endpoint}`,
		json: true,
	};

	query = query || {};

	try {
		if (authenticationMethod === 'accessToken') {
			return await this.helpers.requestWithAuthentication.call(this, 'typeformApi', options);
		} else {
			return await this.helpers.requestOAuth2.call(this, 'typeformOAuth2Api', options);
		}
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

/**
 * Make an API request to paginated Typeform endpoint
 * and return all results
 *
 * @param {(IHookFunctions | IExecuteFunctions)} this
 */
export async function apiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject,
	query?: IDataObject,
	_dataKey?: string,
): Promise<any> {
	if (query === undefined) {
		query = {};
	}

	query.page_size = 200;
	query.page = 0;

	const returnData = {
		items: [] as IDataObject[],
	};

	let responseData;

	do {
		query.page += 1;

		responseData = await apiRequest.call(this, method, endpoint, body, query);

		returnData.items.push.apply(returnData.items, responseData.items as IDataObject[]);
	} while (responseData.page_count !== undefined && responseData.page_count > query.page);

	return returnData;
}

/**
 * Returns all the available forms
 *
 */
export async function getForms(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const endpoint = 'forms';
	const responseData = await apiRequestAllItems.call(this, 'GET', endpoint, {});

	if (responseData.items === undefined) {
		throw new NodeOperationError(this.getNode(), 'No data got returned');
	}

	const returnData: INodePropertyOptions[] = [];
	for (const baseData of responseData.items) {
		returnData.push({
			name: baseData.title,
			value: baseData.id,
		});
	}

	return returnData;
}
