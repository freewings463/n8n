"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/BigQuery/v2/transport/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/BigQuery 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:../../GenericFunctions。导出:无。关键函数/方法:googleBigQueryApiRequest、googleBigQueryApiRequestAllItems。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/BigQuery/v2/transport/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/BigQuery/v2/transport/__init__.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError, NodeOperationError } from 'n8n-workflow';

import { getGoogleAccessToken } from '../../../GenericFunctions';

export async function googleBigQueryApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: IDataObject = {},
	qs: IDataObject = {},
	uri?: string,
	headers: IDataObject = {},
) {
	const authenticationMethod = this.getNodeParameter(
		'authentication',
		0,
		'serviceAccount',
	) as string;

	const options: IRequestOptions = {
		headers: {
			'Content-Type': 'application/json',
		},
		method,
		body,
		qs,
		uri: uri || `https://bigquery.googleapis.com/bigquery${resource}`,
		json: true,
	};
	try {
		if (Object.keys(headers).length !== 0) {
			options.headers = Object.assign({}, options.headers, headers);
		}
		if (Object.keys(body).length === 0) {
			delete options.body;
		}

		if (authenticationMethod === 'serviceAccount') {
			const credentials = await this.getCredentials('googleApi');

			if (credentials === undefined) {
				throw new NodeOperationError(this.getNode(), 'No credentials got returned!');
			}

			const { access_token } = await getGoogleAccessToken.call(this, credentials, 'bigquery');

			options.headers!.Authorization = `Bearer ${access_token}`;
			return await this.helpers.request(options);
		} else {
			return await this.helpers.requestOAuth2.call(this, 'googleBigQueryOAuth2Api', options);
		}
	} catch (error) {
		if (error.code === 'ERR_OSSL_PEM_NO_START_LINE') {
			error.statusCode = '401';
		}

		throw new NodeApiError(this.getNode(), error as JsonObject, {
			message: error?.error?.error?.message || error.message,
		});
	}
}

export async function googleBigQueryApiRequestAllItems(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	query: IDataObject = {},
) {
	let rows: IDataObject[] = [];

	let responseData;
	if (query.maxResults === undefined) {
		query.maxResults = 1000;
	}

	do {
		responseData = await googleBigQueryApiRequest.call(this, method, endpoint, body, query);

		query.pageToken = responseData.pageToken;
		rows = rows.concat((responseData.rows as IDataObject[]) ?? []);
	} while (responseData.pageToken !== undefined && responseData.pageToken !== '');

	return { ...(responseData || {}), rows };
}
