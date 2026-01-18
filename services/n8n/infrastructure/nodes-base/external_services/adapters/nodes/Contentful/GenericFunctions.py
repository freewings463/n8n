"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Contentful/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Contentful 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:contentfulApiRequest、contentfulApiRequestAllItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Contentful/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Contentful/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHttpRequestMethods,
	ILoadOptionsFunctions,
	IRequestOptions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function contentfulApiRequest(
	this: IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	qs: IDataObject = {},
	uri?: string,
	_option: IDataObject = {},
): Promise<any> {
	const credentials = await this.getCredentials('contentfulApi');
	const source = this.getNodeParameter('source', 0) as string;
	const isPreview = source === 'previewApi';

	const options: IRequestOptions = {
		method,
		qs,
		body,
		uri: uri || `https://${isPreview ? 'preview' : 'cdn'}.contentful.com${resource}`,
		json: true,
	};

	if (isPreview) {
		qs.access_token = credentials.ContentPreviewaccessToken as string;
	} else {
		qs.access_token = credentials.ContentDeliveryaccessToken as string;
	}

	try {
		return await this.helpers.request(options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function contentfulApiRequestAllItems(
	this: ILoadOptionsFunctions | IExecuteFunctions,
	propertyName: string,
	method: IHttpRequestMethods,
	resource: string,

	body: any = {},
	query: IDataObject = {},
): Promise<any> {
	const returnData: IDataObject[] = [];

	let responseData;

	query.limit = 100;
	query.skip = 0;

	do {
		responseData = await contentfulApiRequest.call(this, method, resource, body, query);
		query.skip = (query.skip + 1) * query.limit;
		returnData.push.apply(returnData, responseData[propertyName] as IDataObject[]);
	} while (returnData.length < responseData.total);

	return returnData;
}
