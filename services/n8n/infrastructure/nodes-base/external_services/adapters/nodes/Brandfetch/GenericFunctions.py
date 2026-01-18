"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Brandfetch/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Brandfetch 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:brandfetchApiRequest、fetchAndPrepareBinaryData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Brandfetch/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Brandfetch/GenericFunctions.py

import type {
	IDataObject,
	IExecuteFunctions,
	IHookFunctions,
	IHttpRequestMethods,
	IRequestOptions,
	ILoadOptionsFunctions,
	INodeExecutionData,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

export async function brandfetchApiRequest(
	this: IHookFunctions | IExecuteFunctions | ILoadOptionsFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: any = {},
	qs: IDataObject = {},
	uri?: string,
	option: IDataObject = {},
): Promise<any> {
	try {
		let options: IRequestOptions = {
			method,
			qs,
			body,
			url: uri || `https://api.brandfetch.io/v2${resource}`,
			json: true,
		};

		options = Object.assign({}, options, option);

		if (this.getNodeParameter('operation', 0) === 'logo' && options.json === false) {
			delete options.headers;
		}

		if (!Object.keys(body as IDataObject).length) {
			delete options.body;
		}
		if (!Object.keys(qs).length) {
			delete options.qs;
		}

		const response = await this.helpers.requestWithAuthentication.call(
			this,
			'brandfetchApi',
			options,
		);

		if (response.statusCode && response.statusCode !== 200) {
			throw new NodeApiError(this.getNode(), response as JsonObject);
		}

		return response;
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function fetchAndPrepareBinaryData(
	this: IExecuteFunctions,
	imageType: string,
	imageFormat: string,
	logoFormats: IDataObject,
	domain: string,
	newItem: INodeExecutionData,
) {
	const data = await brandfetchApiRequest.call(this, 'GET', '', {}, {}, logoFormats.src as string, {
		json: false,
		encoding: null,
	});

	newItem.binary![`${imageType}_${imageFormat}`] = await this.helpers.prepareBinaryData(
		Buffer.from(data),
		`${imageType}_${domain}.${imageFormat}`,
	);
}
