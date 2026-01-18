"""
MIGRATION-META:
  source_path: packages/core/src/errors/file-not-found.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/errors 的错误。导入/依赖:外部:无；内部:无；本地:./abstract/filesystem.error。导出:FileNotFoundError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Core src/* defaulted to execution engine application services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/errors/file-not-found.error.ts -> services/n8n/application/core/services/execution_engine/errors/file_not_found_error.py

import { FileSystemError } from './abstract/filesystem.error';

export class FileNotFoundError extends FileSystemError {
	constructor(filePath: string) {
		super('File not found', filePath);
	}
}
