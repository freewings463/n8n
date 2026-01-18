"""
MIGRATION-META:
  source_path: packages/@n8n/task-runner/src/js-task-runner/errors/disallowed-module.error.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/task-runner/src/js-task-runner/errors 的错误。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:DisallowedModuleError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Task runner process runtime -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/task-runner/src/js-task-runner/errors/disallowed-module.error.ts -> services/n8n/infrastructure/n8n-task-runner/container/js-task-runner/errors/disallowed_module_error.py

import { UserError } from 'n8n-workflow';

export class DisallowedModuleError extends UserError {
	constructor(moduleName: string) {
		super(`Module '${moduleName}' is disallowed`);
	}
}
