"""
MIGRATION-META:
  source_path: packages/core/src/binary-data/object-store/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/src/binary-data/object-store 的类型。导入/依赖:外部:无；内部:无；本地:../types。导出:MetadataResponseHeaders。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core binary-data storage -> infrastructure file_storage adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/binary-data/object-store/types.ts -> services/n8n/infrastructure/core/external_services/adapters/file_storage/binary_data/object-store/types.py

import type { BinaryData } from '../types';

export type MetadataResponseHeaders = Record<string, string> & {
	'content-length'?: string;
	'content-type'?: string;
	'x-amz-meta-filename'?: string;
	etag?: string;
	'last-modified'?: string;
} & BinaryData.PreWriteMetadata;
