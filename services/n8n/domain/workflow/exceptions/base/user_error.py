"""
MIGRATION-META:
  source_path: packages/workflow/src/errors/base/user.error.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/errors/base 的工作流错误。导入/依赖:外部:无；内部:无；本地:./base.error。导出:UserErrorOptions、UserError。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Workflow errors -> domain/exceptions
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/errors/base/user.error.ts -> services/n8n/domain/workflow/exceptions/base/user_error.py

import type { BaseErrorOptions } from './base.error';
import { BaseError } from './base.error';

export type UserErrorOptions = Omit<BaseErrorOptions, 'level'> & {
	level?: 'info' | 'warning';
	description?: string | null | undefined;
};

/**
 * Error that indicates the user performed an action that caused an error.
 * E.g. provided invalid input, tried to access a resource they’re not
 * authorized to, or violates a business rule.
 *
 * Default level: info
 */
export class UserError extends BaseError {
	declare readonly description: string | null | undefined;

	constructor(message: string, opts: UserErrorOptions = {}) {
		opts.level = opts.level ?? 'info';

		super(message, opts);
	}
}
