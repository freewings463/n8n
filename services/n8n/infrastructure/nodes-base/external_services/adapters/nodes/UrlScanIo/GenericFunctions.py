"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/UrlScanIo/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/UrlScanIo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:normalizeId。关键函数/方法:urlScanIoApiRequest、handleListing、normalizeId。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/UrlScanIo/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/UrlScanIo/GenericFunctions.py

import type { IExecuteFunctions, IDataObject, IRequestOptions } from 'n8n-workflow';

export async function urlScanIoApiRequest(
	this: IExecuteFunctions,
	method: 'GET' | 'POST',
	endpoint: string,
	body: IDataObject = {},
	qs: IDataObject = {},
) {
	const options: IRequestOptions = {
		method,
		body,
		qs,
		uri: `https://urlscan.io/api/v1${endpoint}`,
		json: true,
	};

	if (!Object.keys(body).length) {
		delete options.body;
	}

	if (!Object.keys(qs).length) {
		delete options.qs;
	}

	return await this.helpers.requestWithAuthentication.call(this, 'urlScanIoApi', options);
}

export async function handleListing(
	this: IExecuteFunctions,
	endpoint: string,
	qs: IDataObject = {},
): Promise<IDataObject[]> {
	const returnData: IDataObject[] = [];
	let responseData;

	qs.size = 100;

	const returnAll = this.getNodeParameter('returnAll', 0, false);
	const limit = this.getNodeParameter('limit', 0, 0);

	do {
		responseData = await urlScanIoApiRequest.call(this, 'GET', endpoint, {}, qs);
		returnData.push(...(responseData.results as IDataObject[]));

		if (!returnAll && returnData.length > limit) {
			return returnData.slice(0, limit);
		}

		if (responseData.results.length) {
			const lastResult = responseData.results[responseData.results.length - 1];
			qs.search_after = lastResult.sort;
		}
	} while (responseData.total > returnData.length);

	return returnData;
}

export const normalizeId = ({ _id, uuid, ...rest }: IDataObject) => {
	if (_id) return { scanId: _id, ...rest };
	if (uuid) return { scanId: uuid, ...rest };
	return rest;
};
