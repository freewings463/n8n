"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/WhatsApp/MediaFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/WhatsApp 的节点。导入/依赖:外部:form-data；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:getUploadFormData、mediaPropertyName、mediaFileName、setupUpload。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/WhatsApp/MediaFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/WhatsApp/MediaFunctions.py

import FormData from 'form-data';
import type { IDataObject, IExecuteSingleFunctions, IHttpRequestOptions } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

export async function getUploadFormData(
	this: IExecuteSingleFunctions,
): Promise<{ fileName: string; formData: FormData }> {
	const mediaPropertyName = ((this.getNodeParameter('mediaPropertyName') as string) || '').trim();
	if (!mediaPropertyName)
		throw new NodeOperationError(this.getNode(), 'Parameter "mediaPropertyName" is not defined');

	const binaryData = this.helpers.assertBinaryData(mediaPropertyName);

	const mediaFileName = (this.getNodeParameter('additionalFields') as IDataObject).mediaFileName as
		| string
		| undefined;

	const fileName = mediaFileName || binaryData.fileName;
	if (!fileName)
		throw new NodeOperationError(this.getNode(), 'No file name given for media upload.');

	const buffer = await this.helpers.getBinaryDataBuffer(mediaPropertyName);

	const formData = new FormData();
	formData.append('file', buffer, { contentType: binaryData.mimeType, filename: fileName });
	formData.append('messaging_product', 'whatsapp');

	return { fileName, formData };
}

export async function setupUpload(
	this: IExecuteSingleFunctions,
	requestOptions: IHttpRequestOptions,
) {
	const uploadData = await getUploadFormData.call(this);
	requestOptions.body = uploadData.formData;
	return requestOptions;
}
