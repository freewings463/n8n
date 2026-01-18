"""
MIGRATION-META:
  source_path: packages/core/src/utils/serialized-buffer.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/utils 的工具。导入/依赖:外部:无；内部:@n8n/backend-common；本地:无。导出:SerializedBuffer、toBuffer、isSerializedBuffer。关键函数/方法:toBuffer、isSerializedBuffer、isObjectLiteral。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Core utility helpers -> application/services/utils
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/utils/serialized-buffer.ts -> services/n8n/application/core/services/utils/serialized_buffer.py

import { isObjectLiteral } from '@n8n/backend-common';

/** A nodejs Buffer gone through JSON.stringify */
export type SerializedBuffer = {
	type: 'Buffer';
	data: number[]; // Array like Uint8Array, each item is uint8 (0-255)
};

/** Converts the given SerializedBuffer to nodejs Buffer */
export function toBuffer(serializedBuffer: SerializedBuffer): Buffer {
	return Buffer.from(serializedBuffer.data);
}

export function isSerializedBuffer(candidate: unknown): candidate is SerializedBuffer {
	return (
		isObjectLiteral(candidate) &&
		'type' in candidate &&
		'data' in candidate &&
		candidate.type === 'Buffer' &&
		Array.isArray(candidate.data)
	);
}
