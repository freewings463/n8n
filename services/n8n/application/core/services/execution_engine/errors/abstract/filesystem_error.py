"""
MIGRATION-META:
  source_path: packages/core/src/errors/abstract/filesystem.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/errors/abstract 的错误。导入/依赖:外部:无；内部:@n8n/errors；本地:无。导出:无。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Core src/* defaulted to execution engine application services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/errors/abstract/filesystem.error.ts -> services/n8n/application/core/services/execution_engine/errors/abstract/filesystem_error.py

import { ApplicationError } from '@n8n/errors';

export abstract class FileSystemError extends ApplicationError {
	constructor(message: string, filePath: string) {
		super(message, { extra: { filePath } });
	}
}
