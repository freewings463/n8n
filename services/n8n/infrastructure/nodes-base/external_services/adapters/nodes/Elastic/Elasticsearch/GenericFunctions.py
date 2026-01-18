"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Elastic/Elasticsearch/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Elastic/Elasticsearch 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./types。导出:无。关键函数/方法:elasticsearchBulkApiRequest、elasticsearchApiRequest、elasticsearchApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Elastic/Elasticsearch/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Elastic/Elasticsearch/GenericFunctions.py

import type {
	IExecuteFunctions,
	IDataObject,
	JsonObject,
	IHttpRequestOptions,
	IHttpRequestMethods,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

import type { ElasticsearchApiCredentials } from './types';

export async function elasticsearchBulkApiRequest(this: IExecuteFunctions, body: IDataObject) {
	const { baseUrl, ignoreSSLIssues } =
		await this.getCredentials<ElasticsearchApiCredentials>('elasticsearchApi');

	const bulkBody = Object.values(body).flat().join('\n') + '\n';

	const options: IHttpRequestOptions = {
		method: 'POST',
		headers: { 'Content-Type': 'application/x-ndjson' },
		body: bulkBody,
		url: `${baseUrl.replace(/\/$/, '')}/_bulk`,
		skipSslCertificateValidation: ignoreSSLIssues,
		returnFullResponse: true,
		ignoreHttpStatusErrors: true,
	};

	const response = await this.helpers.httpRequestWithAuthentication.call(
		this,
		'elasticsearchApi',
		options,
	);

	if (response.statusCode > 299) {
		if (this.continueOnFail()) {
			return Object.values(body).map((_) => ({ error: response.body.error }));
		} else {
			throw new NodeApiError(this.getNode(), { error: response.body.error } as JsonObject);
		}
	}

	return response.body.items.map((item: IDataObject) => {
		return {
			...(item.index as IDataObject),
			...(item.update as IDataObject),
			...(item.create as IDataObject),
			...(item.delete as IDataObject),
			...(item.error as IDataObject),
		};
	});
}

export async function elasticsearchApiRequest(
	this: IExecuteFunctions,
	method: IHttpRequestMethods,
	endpoint: string,
	body: IDataObject = {},
	qs: IDataObject = {},
) {
	const { baseUrl, ignoreSSLIssues } =
		await this.getCredentials<ElasticsearchApiCredentials>('elasticsearchApi');

	const options: IHttpRequestOptions = {
		method,
		body,
		qs,
		url: `${baseUrl.replace(/\/$/, '')}${endpoint}`,
		json: true,
		skipSslCertificateValidation: ignoreSSLIssues,
	};

	if (!Object.keys(body).length) {
		delete options.body;
	}

	if (!Object.keys(qs).length) {
		delete options.qs;
	}

	try {
		return await this.helpers.httpRequestWithAuthentication.call(this, 'elasticsearchApi', options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function elasticsearchApiRequestAllItems(
	this: IExecuteFunctions,
	indexId: string,
	body: IDataObject = {},
	qs: IDataObject = {},
): Promise<any> {
	//https://www.elastic.co/guide/en/elasticsearch/reference/7.16/paginate-search-results.html#search-after
	try {
		//create a point in time (PIT) to preserve the current index state over your searches
		let pit = (
			await elasticsearchApiRequest.call(this, 'POST', `/${indexId}/_pit`, {}, { keep_alive: '1m' })
		)?.id as string;

		let returnData: IDataObject[] = [];
		let responseData;
		let searchAfter: string[] = [];

		const requestBody: IDataObject = {
			...body,
			size: 10000,
			pit: {
				id: pit,
				keep_alive: '1m',
			},
			track_total_hits: false, //Disable the tracking of total hits to speed up pagination
		};

		responseData = await elasticsearchApiRequest.call(this, 'POST', '/_search', requestBody, qs);
		if (responseData?.hits?.hits) {
			returnData = returnData.concat(responseData.hits.hits as IDataObject[]);
			const lastHitIndex = responseData.hits.hits.length - 1;
			//Sort values for the last returned hit with the tiebreaker value
			searchAfter = responseData.hits.hits[lastHitIndex].sort;
			//Update id for the point in time
			pit = responseData.pit_id;
		} else {
			return [];
		}

		while (true) {
			requestBody.search_after = searchAfter;
			requestBody.pit = { id: pit, keep_alive: '1m' };

			responseData = await elasticsearchApiRequest.call(this, 'POST', '/_search', requestBody, qs);

			if (responseData?.hits?.hits?.length) {
				returnData = returnData.concat(responseData.hits.hits as IDataObject[]);
				const lastHitIndex = responseData.hits.hits.length - 1;
				searchAfter = responseData.hits.hits[lastHitIndex].sort;
				pit = responseData.pit_id;
			} else {
				break;
			}
		}

		await elasticsearchApiRequest.call(this, 'DELETE', '/_pit', { id: pit });

		return returnData;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}
