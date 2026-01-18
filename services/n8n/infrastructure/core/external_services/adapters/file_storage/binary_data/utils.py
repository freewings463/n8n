"""
MIGRATION-META:
  source_path: packages/core/src/binary-data/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/src/binary-data 的模块。导入/依赖:外部:node:fs/promises；内部:n8n-workflow；本地:./types。导出:isStoredMode、FileLocation。关键函数/方法:isStoredMode、assertDir、doesNotExist、streamToBuffer、reject、binaryToBuffer。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected binary data storage IO -> infrastructure file_storage adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/binary-data/utils.ts -> services/n8n/infrastructure/core/external_services/adapters/file_storage/binary_data/utils.py

import { UnexpectedError } from 'n8n-workflow';
import fs from 'node:fs/promises';
import type { Readable } from 'node:stream';

import type { BinaryData } from './types';

const STORED_MODES = ['filesystem', 'filesystem-v2', 's3', 'database'] as const;

export function isStoredMode(mode: string): mode is BinaryData.StoredMode {
	return STORED_MODES.includes(mode as BinaryData.StoredMode);
}

export async function assertDir(dir: string) {
	try {
		await fs.access(dir);
	} catch {
		await fs.mkdir(dir, { recursive: true });
	}
}

export async function doesNotExist(dir: string) {
	try {
		await fs.access(dir);
		return false;
	} catch {
		return true;
	}
}

/** Converts a readable stream to a buffer */
export async function streamToBuffer(stream: Readable) {
	return await new Promise<Buffer>((resolve, reject) => {
		const chunks: Buffer[] = [];
		stream.on('data', (chunk: Buffer) => chunks.push(chunk));
		stream.on('end', () => resolve(Buffer.concat(chunks)));
		stream.once('error', (cause) => {
			if ('code' in cause && cause.code === 'Z_DATA_ERROR')
				reject(new UnexpectedError('Failed to decompress response', { cause }));
			else reject(cause);
		});
	});
}

/** Converts a buffer or a readable stream to a buffer */
export async function binaryToBuffer(body: Buffer | Readable) {
	if (Buffer.isBuffer(body)) return body;
	return await streamToBuffer(body);
}

export const FileLocation = {
	ofExecution: (workflowId: string, executionId: string): BinaryData.FileLocation => ({
		type: 'execution',
		workflowId,
		executionId,
	}),

	/**
	 * Create a location for a binary file at a custom path,
	 * e.g. ["chat-hub", "sessions", "abc", "messages", "def"] -> "chat-hub/sessions/abc/messages/def"
	 */
	ofCustom: ({
		pathSegments,
		sourceType,
		sourceId,
	}: {
		pathSegments: string[];
		sourceType?: string;
		sourceId?: string;
	}): BinaryData.FileLocation => ({
		type: 'custom',
		pathSegments,
		sourceType,
		sourceId,
	}),
};
