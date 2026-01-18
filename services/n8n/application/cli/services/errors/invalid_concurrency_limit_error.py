"""
MIGRATION-META:
  source_path: packages/cli/src/errors/invalid-concurrency-limit.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/errors 的错误。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:InvalidConcurrencyLimitError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/errors/invalid-concurrency-limit.error.ts -> services/n8n/application/cli/services/errors/invalid_concurrency_limit_error.py

import { UserError } from 'n8n-workflow';

export class InvalidConcurrencyLimitError extends UserError {
	constructor(value: number) {
		super('Concurrency limit set to invalid value', { extra: { value } });
	}
}
