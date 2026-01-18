"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/helpers/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/Anthropic 的节点。导入/依赖:外部:form-data；内部:n8n-workflow；本地:../transport、./interfaces。导出:getMimeType、splitByComma。关键函数/方法:getMimeType、downloadFile、downloadResponse、uploadFile、splitByComma、getBaseUrl。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/helpers/utils.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/Anthropic/helpers/utils.py

import FormData from 'form-data';
import type { IDataObject, IExecuteFunctions, ILoadOptionsFunctions } from 'n8n-workflow';

import { apiRequest } from '../transport';
import type { File } from './interfaces';

export function getMimeType(contentType?: string) {
	return contentType?.split(';')?.[0];
}

export async function downloadFile(this: IExecuteFunctions, url: string, qs?: IDataObject) {
	const downloadResponse = (await this.helpers.httpRequest({
		method: 'GET',
		url,
		qs,
		returnFullResponse: true,
		encoding: 'arraybuffer',
	})) as { body: ArrayBuffer; headers: IDataObject };

	const mimeType =
		getMimeType(downloadResponse.headers?.['content-type'] as string) ?? 'application/octet-stream';
	const fileContent = Buffer.from(downloadResponse.body);
	return {
		fileContent,
		mimeType,
	};
}

export async function uploadFile(
	this: IExecuteFunctions,
	fileContent: Buffer,
	mimeType: string,
	fileName?: string,
) {
	const form = new FormData();
	form.append('file', fileContent, {
		filename: fileName ?? 'file',
		contentType: mimeType,
	});
	return (await apiRequest.call(this, 'POST', '/v1/files', {
		headers: form.getHeaders(),
		body: form,
	})) as File;
}

export function splitByComma(str: string) {
	return str
		.split(',')
		.map((s) => s.trim())
		.filter((s) => s);
}

export async function getBaseUrl(this: IExecuteFunctions | ILoadOptionsFunctions) {
	const credentials = await this.getCredentials('anthropicApi');
	return (credentials.url ?? 'https://api.anthropic.com') as string;
}
