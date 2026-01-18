"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/RespondToWebhook/utils/binary.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/RespondToWebhook/utils 的工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:getBinaryResponse。关键函数/方法:setContentLength、getBinaryResponse。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/RespondToWebhook/utils/binary.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/RespondToWebhook/utils/binary.py

import type { IBinaryData, IDataObject, IN8nHttpResponse } from 'n8n-workflow';
import { BINARY_ENCODING } from 'n8n-workflow';
import type { Readable } from 'stream';

const setContentLength = (responseBody: IN8nHttpResponse | Readable, headers: IDataObject) => {
	if (Buffer.isBuffer(responseBody)) {
		headers['content-length'] = responseBody.length;
	} else if (typeof responseBody === 'string') {
		headers['content-length'] = Buffer.byteLength(responseBody, 'utf8');
	}
};

/**
 * Returns a response body for a binary data and sets the content-type header.
 */
export const getBinaryResponse = (binaryData: IBinaryData, headers: IDataObject) => {
	let responseBody: IN8nHttpResponse | Readable;

	if (binaryData.id) {
		responseBody = { binaryData };
	} else {
		const responseBuffer = Buffer.from(binaryData.data, BINARY_ENCODING);
		responseBody = responseBuffer;
		setContentLength(responseBody, headers);
	}

	headers['content-type'] ??= binaryData.mimeType;

	return responseBody;
};
