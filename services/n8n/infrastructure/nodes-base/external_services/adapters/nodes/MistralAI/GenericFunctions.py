"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MistralAI/GenericFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MistralAI 的节点。导入/依赖:外部:form-data；内部:n8n-workflow；本地:./types。导出:processResponseData。关键函数/方法:mistralApiRequest、encodeBinaryData、processResponseData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MistralAI/GenericFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MistralAI/GenericFunctions.py

import type FormData from 'form-data';
import type {
	IDataObject,
	IExecuteFunctions,
	IHttpRequestMethods,
	IHttpRequestOptions,
	JsonObject,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

import type { Page } from './types';

export async function mistralApiRequest(
	this: IExecuteFunctions,
	method: IHttpRequestMethods,
	resource: string,
	body: IDataObject | FormData = {},
	qs: IDataObject = {},
): Promise<any> {
	const options: IHttpRequestOptions = {
		method,
		body,
		qs,
		url: `https://api.mistral.ai${resource}`,
		json: true,
	};

	if (Object.keys(body).length === 0) {
		delete options.body;
	}
	if (Object.keys(qs).length === 0) {
		delete options.qs;
	}

	try {
		return await this.helpers.httpRequestWithAuthentication.call(this, 'mistralCloudApi', options);
	} catch (error) {
		throw new NodeApiError(this.getNode(), error as JsonObject);
	}
}

export async function encodeBinaryData(
	this: IExecuteFunctions,
	itemIndex: number,
): Promise<{ dataUrl: string; fileName: string | undefined }> {
	const binaryProperty = this.getNodeParameter('binaryProperty', itemIndex);
	const binaryData = this.helpers.assertBinaryData(itemIndex, binaryProperty);
	const binaryDataBuffer = await this.helpers.getBinaryDataBuffer(itemIndex, binaryProperty);
	const base64Data = binaryDataBuffer.toString('base64');
	const dataUrl = `data:${binaryData.mimeType};base64,${base64Data}`;

	return { dataUrl, fileName: binaryData.fileName };
}

export function processResponseData(response: IDataObject): IDataObject {
	const pages = response.pages as Page[];
	return {
		...response,
		extractedText: pages.map((page) => page.markdown).join('\n\n'),
		pageCount: pages.length,
	};
}
