"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Firebase/RealtimeDatabase/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Firebase 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:googleApiRequest、googleApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Firebase/RealtimeDatabase/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Firebase/RealtimeDatabase/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function googleApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	projectId: string,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	qs: IDataObject = {},
	headers: IDataObject = {},
	uri: string | null = null,
): Promise<any> {
	const { region } = await this.getCredentials('googleFirebaseRealtimeDatabaseOAuth2Api');

	const options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
		},
		method,
		body,
		qs,
		url: uri || `https://${projectId}.${region}/${resource}.json`,
		json: true,
	};

	try {
		if (Object.keys(headers).length !== 0) {
			options.headers = Object.assign({}, options.headers, headers);
		}
		if (Object.keys(body as IDataObject).length === 0) {
			delete options.body;
		}

		return await this.helpers.requestOAuth2.call(
			this,
			'googleFirebaseRealtimeDatabaseOAuth2Api',
			options,
		);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function googleApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	projectId: string,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	qs: IDataObject = {},
	_headers: IDataObject = {},
	uri: string | null = null,
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;
	qs.pageSize = 100;

	do {
		responseData = await googleApiRequest.call(
			this,
			projectId,
			method,
			resource,
			body,
			qs,
			{},
			uri,
		);
		qs.pageToken = responseData.nextPageToken;
		returnData.push.apply(returnData, responseData[resource] as IDataObject[]);
	} while (responseData.nextPageToken !== undefined && responseData.nextPageToken !== '');

	return returnData;
}
