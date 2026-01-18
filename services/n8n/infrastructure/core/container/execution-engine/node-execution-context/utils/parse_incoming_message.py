"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/utils/parse-incoming-message.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context/utils 的执行工具。导入/依赖:外部:无；内部:无；本地:无。导出:parseContentType、parseContentDisposition、parseIncomingMessage。关键函数/方法:parseHeaderParameters、parseContentType、parseContentDisposition、parseIncomingMessage。用于提供执行通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/utils/parse-incoming-message.ts -> services/n8n/infrastructure/core/container/execution-engine/node-execution-context/utils/parse_incoming_message.py

import type { IncomingMessage } from 'http';

function parseHeaderParameters(parameters: string[]): Record<string, string> {
	return parameters.reduce(
		(acc, param) => {
			const [key, value] = param.split('=');
			let decodedValue = decodeURIComponent(value).trim();
			if (decodedValue.startsWith('"') && decodedValue.endsWith('"')) {
				decodedValue = decodedValue.slice(1, -1);
			}
			acc[key.toLowerCase().trim()] = decodedValue;
			return acc;
		},
		{} as Record<string, string>,
	);
}

interface IContentType {
	type: string;
	parameters: {
		charset: string;
		[key: string]: string;
	};
}

/**
 * Parses the Content-Type header string into a structured object
 * @returns {IContentType | null} Parsed content type details or null if no content type is detected
 */
export const parseContentType = (contentType?: string): IContentType | null => {
	if (!contentType) {
		return null;
	}

	const [type, ...parameters] = contentType.split(';');

	return {
		type: type.toLowerCase(),
		parameters: { charset: 'utf-8', ...parseHeaderParameters(parameters) },
	};
};

interface IContentDisposition {
	type: string;
	filename?: string;
}

/**
 * Parses the Content-Disposition header string into a structured object
 * @returns {IContentDisposition | null} Parsed content disposition details or null if no content disposition is detected
 */
export const parseContentDisposition = (
	contentDisposition?: string,
): IContentDisposition | null => {
	if (!contentDisposition) {
		return null;
	}

	// This is invalid syntax, but common
	// Example 'filename="example.png"' (instead of 'attachment; filename="example.png"')
	if (!contentDisposition.startsWith('attachment') && !contentDisposition.startsWith('inline')) {
		contentDisposition = `attachment; ${contentDisposition}`;
	}

	const [type, ...parameters] = contentDisposition.split(';');

	const parsedParameters = parseHeaderParameters(parameters);

	let { filename } = parsedParameters;
	const wildcard = parsedParameters['filename*'];
	if (wildcard) {
		// https://datatracker.ietf.org/doc/html/rfc5987
		const [_encoding, _locale, content] = wildcard?.split("'") ?? [];
		filename = content;
	}

	return { type, filename };
};

/**
 * Augments an IncomingMessage with parsed content type and disposition information
 */
export function parseIncomingMessage(message: IncomingMessage) {
	const contentType = parseContentType(message.headers['content-type']);
	if (contentType) {
		const { type, parameters } = contentType;
		message.contentType = type;
		message.encoding = parameters.charset.toLowerCase() as BufferEncoding;
	}

	const contentDisposition = parseContentDisposition(message.headers['content-disposition']);
	if (contentDisposition) {
		message.contentDisposition = contentDisposition;
	}
}
