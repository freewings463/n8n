"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/errors.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src 的模块。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:NonMethodError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/errors.ts -> services/n8n/infrastructure/n8n-decorators/container/src/errors.py

import { UnexpectedError } from 'n8n-workflow';

export class NonMethodError extends UnexpectedError {
	constructor(name: string) {
		super(`${name} must be a method on a class to use this decorator`);
	}
}
