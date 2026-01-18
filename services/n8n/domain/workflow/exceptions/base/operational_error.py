"""
MIGRATION-META:
  source_path: packages/workflow/src/errors/base/operational.error.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/errors/base 的工作流错误。导入/依赖:外部:无；内部:无；本地:./base.error。导出:OperationalErrorOptions、OperationalError。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Workflow errors -> domain/exceptions
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/errors/base/operational.error.ts -> services/n8n/domain/workflow/exceptions/base/operational_error.py

import type { BaseErrorOptions } from './base.error';
import { BaseError } from './base.error';

export type OperationalErrorOptions = Omit<BaseErrorOptions, 'level'> & {
	level?: 'info' | 'warning' | 'error';
};

/**
 * Error that indicates a transient issue, like a network request failing,
 * a database query timing out, etc. These are expected to happen, are
 * transient by nature and should be handled gracefully.
 *
 * Default level: warning
 */
export class OperationalError extends BaseError {
	constructor(message: string, opts: OperationalErrorOptions = {}) {
		opts.level = opts.level ?? 'warning';

		super(message, opts);
	}
}
