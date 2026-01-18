"""
MIGRATION-META:
  source_path: packages/core/src/errors/invalid-execution-metadata.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/errors 的执行错误。导入/依赖:外部:无；内部:@n8n/errors；本地:无。导出:InvalidExecutionMetadataError。关键函数/方法:无。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Core src/* defaulted to execution engine application services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/errors/invalid-execution-metadata.error.ts -> services/n8n/application/core/services/execution_engine/errors/invalid_execution_metadata_error.py

import { ApplicationError } from '@n8n/errors';

export class InvalidExecutionMetadataError extends ApplicationError {
	constructor(
		public type: 'key' | 'value',
		key: unknown,
		message?: string,
		options?: ErrorOptions,
	) {
		// eslint-disable-next-line @typescript-eslint/restrict-template-expressions
		super(message ?? `Custom data ${type}s must be a string (key "${key}")`, options);
	}
}
