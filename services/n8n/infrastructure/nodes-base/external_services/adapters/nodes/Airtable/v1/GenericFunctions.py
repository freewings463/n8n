"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtable/v1/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtable/v1 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:IRecord。关键函数/方法:apiRequest、apiRequestAllItems、downloadRecordAttachments。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtable/v1/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtable/v1/GenericFunctions.py

import type {
	IBinaryKeyData,
	IDataObject,
	IExecuteFunctions,
	IPollFunctions,
	ILoadOptionsFunctions,
	INodeExecutionData,
	IPairedItemData,
	IRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';

interface IAttachment {
	url: string;
	filename: string;
	type: string;
}

export interface IRecord {
	fields: {
		[key: string]: string | IAttachment[];
	};
}

/**
 * Make an API request to Airtable
 *
 */
export async function apiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions | IPollFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: object,
	query?: IDataObject,
	uri?: string,
	option: IDataObject = {},
): Promise<any> {
	query = query || {};

	// For some reason for some endpoints the bearer auth does not work
	// and it returns 404 like for the /meta request. So we always send
	// it as query string.
	// query.api_key = credentials.apiKey;

	const options: IRequestOptions = {
		headers: {},
		method,
		body,
		qs: query,
		uri: uri || `https://api.airtable.com/v0/${endpoint}`,
		useQuerystring: false,
		json: true,
	};

	if (Object.keys(option).length !== 0) {
		Object.assign(options, option);
	}

	if (Object.keys(body).length === 0) {
		delete options.body;
	}
	const authenticationMethod = this.getNodeParameter('authentication', 0) as string;
	return await this.helpers.requestWithAuthentication.call(this, authenticationMethod, options);
}

/**
 * Make an API request to paginated Airtable endpoint
 * and return all results
 *
 * @param {(IExecuteFunctions | IExecuteFunctions)} this
 */
export async function apiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions | IPollFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject,
	query?: IDataObject,
): Promise<any> {
	if (query === undefined) {
		query = {};
	}
	query.pageSize = 100;

	const returnData: IDataObject[] = [];

	let responseData;

	do {
		responseData = await apiRequest.call(this, method, endpoint, body, query);
		returnData.push.apply(returnData, responseData.records as IDataObject[]);

		query.offset = responseData.offset;
	} while (responseData.offset !== undefined);

	return {
		records: returnData,
	};
}

export async function downloadRecordAttachments(
	this: IExecuteFunctions | IPollFunctions,
	records: IRecord[],
	fieldNames: string[],
	pairedItem?: IPairedItemData[],
): Promise<INodeExecutionData[]> {
	const elements: INodeExecutionData[] = [];
	for (const record of records) {
		const element: INodeExecutionData = { json: {}, binary: {} };
		if (pairedItem) {
			element.pairedItem = pairedItem;
		}
		element.json = record as unknown as IDataObject;
		for (const fieldName of fieldNames) {
			if (record.fields[fieldName] !== undefined) {
				for (const [index, attachment] of (record.fields[fieldName] as IAttachment[]).entries()) {
					const file = await apiRequest.call(this, 'GET', '', {}, {}, attachment.url, {
						json: false,
						encoding: null,
					});
					element.binary![`${fieldName}_${index}`] = await this.helpers.prepareBinaryData(
						Buffer.from(file as string),
						attachment.filename,
						attachment.type,
					);
				}
			}
		}
		if (Object.keys(element.binary as IBinaryKeyData).length === 0) {
			delete element.binary;
		}
		elements.push(element);
	}
	return elements;
}
