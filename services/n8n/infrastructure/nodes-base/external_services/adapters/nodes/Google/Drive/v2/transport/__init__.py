"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Drive/v2/transport/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Drive 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:../../GenericFunctions。导出:无。关键函数/方法:googleApiRequest、googleApiRequestAllItems。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Drive/v2/transport/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Drive/v2/transport/__init__.py

import type {
	IExecuteFunctions,
	ILoadOptionsFunctions,
	IDataObject,
	IPollFunctions,
	JsonObject,
	IHttpRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

import { getGoogleAccessToken } from '../../../GenericFunctions';

export async function googleApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions | IPollFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: IDataObject | string | Buffer = {},
	qs: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
) {
	const authenticationMethod = this.getNodeParameter(
		'authentication',
		0,
		'serviceAccount',
	) as string;

	let options: IHttpRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
		},
		method,
		body,
		qs,
		url: uri || `https://www.googleapis.com${resource}`,
		json: true,
	};

	options = Object.assign({}, options, option);
	try {
		if (Object.keys(body).length === 0) {
			delete options.body;
		}

		if (authenticationMethod === 'serviceAccount') {
			const credentials = await this.getCredentials('googleApi');

			const { access_token } = await getGoogleAccessToken.call(this, credentials, 'drive');

			options.headers!.Authorization = `Bearer ${access_token}`;
			return await this.helpers.httpRequest(options);
		} else {
			return await this.helpers.httpRequestWithAuthentication.call(
				this,
				'googleDriveOAuth2Api',
				options,
			);
		}
	} catch (error) {
		if (error.code === 'ERR_OSSL_PEM_NO_START_LINE') {
			error.statusCode = '401';
		}

		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function googleApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions | IPollFunctions,
	method: IHttpRequestMethods,
	propertyName: string,
	endpoint: string,
	body: IDataObject = {},
	query: IDataObject = {},
) {
	const returnData: IDataObject[] = [];

	let responseData;
	query.maxResults = query.maxResults || 100;
	query.pageSize = query.pageSize || 100;

	do {
		responseData = await googleApiRequest.call(this, method, endpoint, body, query);
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);

		if (responseData.nextPageToken) {
			query.pageToken = responseData.nextPageToken as string;
		}
	} while (responseData.nextPageToken !== undefined && responseData.nextPageToken !== '');

	return returnData;
}
