"""
MIGRATION-META:
  source_path: packages/cli/src/webhooks/webhook-form-data.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/webhooks 的Webhook模块。导入/依赖:外部:formidable；内部:无；本地:无。导出:createMultiFormDataParser。关键函数/方法:createMultiFormDataParser、normalizeFormData、resolve。用于承载Webhook实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/webhooks/webhook-form-data.ts -> services/n8n/infrastructure/cli/container/webhooks/webhook_form_data.py

import formidable from 'formidable';
import type { IncomingMessage } from 'http';

const normalizeFormData = <T>(values: Record<string, T | T[]>) => {
	for (const key in values) {
		const value = values[key];
		if (Array.isArray(value) && value.length === 1) {
			values[key] = value[0];
		}
	}
};

/**
 * Creates a function that parses the multipart form data into the request's `body` property
 */
export const createMultiFormDataParser = (maxFormDataSizeInMb: number) => {
	return async function parseMultipartFormData(req: IncomingMessage): Promise<{
		data: formidable.Fields;
		files: formidable.Files;
	}> {
		const { encoding } = req;

		const form = formidable({
			multiples: true,
			encoding: encoding as formidable.BufferEncoding,
			maxFileSize: maxFormDataSizeInMb * 1024 * 1024,
			// TODO: pass a custom `fileWriteStreamHandler` to create binary data files directly
		});

		return await new Promise((resolve) => {
			form.parse(req, async (_err, data, files) => {
				normalizeFormData(data);
				normalizeFormData(files);
				resolve({ data, files });
			});
		});
	};
};
