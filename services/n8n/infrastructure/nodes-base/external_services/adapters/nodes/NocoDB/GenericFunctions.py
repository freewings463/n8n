"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/NocoDB/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/NocoDB 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:apiRequest、apiRequestAllItems、downloadRecordAttachments。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/NocoDB/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/NocoDB/GenericFunctions.py

import type {
	IBinaryKeyData,
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	INodeExecutionData,
	IPairedItemData,
	IPollFunctions,
	IRequestOptions,
} from 'n8n-workflow';
import { jsonParse, NodeOperationError } from 'n8n-workflow';

interface IAttachment {
	url: string;
	title: string;
	mimetype: string;
	size: number;
	signedUrl?: string;
}

/**
 * Make an API request to NocoDB
 *
 */
export async function apiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions | IPollFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: object,
	query?: IDataObject,
	uri?: string,
	option: IDataObject = {},
): Promise<any> {
	const authenticationMethod = this.getNodeParameter('authentication', 0) as string;
	const credentials = await this.getCredentials(authenticationMethod);

	if (credentials === undefined) {
		throw new NodeOperationError(this.getNode(), 'No credentials got returned!');
	}

	const baseUrl = credentials.host as string;

	query = query || {};

	if (!uri) {
		uri = baseUrl.endsWith('/') ? `${baseUrl.slice(0, -1)}${endpoint}` : `${baseUrl}${endpoint}`;
	}

	const options: IRequestOptions = {
		method,
		body,
		qs: query,
		uri,
		json: true,
	};

	if (Object.keys(option).length !== 0) {
		Object.assign(options, option);
	}

	if (Object.keys(body).length === 0) {
		delete options.body;
	}

	return await this.helpers.requestWithAuthentication.call(this, authenticationMethod, options);
}

/**
 * Make an API request to paginated NocoDB endpoint
 * and return all results
 *
 * @param {(IHookFunctions | IExecuteFunctions)} this
 */
export async function apiRequestAllItems(
	this: IHookFunctions | IExecuteFunctions | IPollFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject,
	query?: IDataObject,
): Promise<any> {
	const version = this.getNode().typeVersion;

	if (query === undefined) {
		query = {};
	}
	query.limit = 100;
	query.offset = query?.offset ? (query.offset as number) : 0;
	const returnData: IDataObject[] = [];

	let responseData;

	do {
		responseData = await apiRequest.call(this, method, endpoint, body, query);
		version === 1
			? returnData.push(...(responseData as IDataObject[]))
			: returnData.push(...(responseData.list as IDataObject[]));

		query.offset += query.limit;
	} while (version === 1 ? responseData.length !== 0 : responseData.pageInfo.isLastPage !== true);

	return returnData;
}

export async function downloadRecordAttachments(
	this: IExecuteFunctions | IPollFunctions,
	records: IDataObject[],
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
			let attachments = record[fieldName] as IAttachment[];
			if (typeof attachments === 'string') {
				attachments = jsonParse<IAttachment[]>(record[fieldName] as string);
			}
			if (record[fieldName]) {
				for (const [index, attachment] of attachments.entries()) {
					const attachmentUrl = attachment.signedUrl || attachment.url;
					const file: Buffer = await apiRequest.call(this, 'GET', '', {}, {}, attachmentUrl, {
						json: false,
						encoding: null,
					});
					element.binary![`${fieldName}_${index}`] = await this.helpers.prepareBinaryData(
						Buffer.from(file),
						attachment.title,
						attachment.mimetype,
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
