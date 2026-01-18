"""
MIGRATION-META:
  source_path: packages/core/src/errors/file-too-large.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/errors 的错误。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:FileTooLargeError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Core src/* defaulted to execution engine application services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/errors/file-too-large.error.ts -> services/n8n/application/core/services/execution_engine/errors/file_too_large_error.py

import { UserError } from 'n8n-workflow';

export class FileTooLargeError extends UserError {
	constructor({
		fileSizeMb,
		maxFileSizeMb,
		fileId,
		fileName,
	}: {
		fileSizeMb: number;
		maxFileSizeMb: number;
		fileId: string;
		fileName?: string;
	}) {
		const id = fileName ? `"${fileName}" (${fileId})` : fileId;
		const roundedSize = Math.round(fileSizeMb * 100) / 100;
		super(
			`Failed to write binary file ${id} because its size of ${roundedSize} MB exceeds the max size limit of ${maxFileSizeMb} MB set for \`database\` mode. Consider increasing \`N8N_BINARY_DATA_DATABASE_MAX_FILE_SIZE\` up to 1 GB, or using S3 storage mode if you require writes larger than 1 GB.`,
		);
	}
}
