"""
MIGRATION-META:
  source_path: packages/cli/src/errors/response-errors/invalid-mfa-recovery-code-error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/errors/response-errors 的错误。导入/依赖:外部:无；内部:无；本地:./forbidden.error。导出:InvalidMfaRecoveryCodeError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/errors/response-errors/invalid-mfa-recovery-code-error.ts -> services/n8n/application/cli/services/errors/response-errors/invalid_mfa_recovery_code_error.py

import { ForbiddenError } from './forbidden.error';

export class InvalidMfaRecoveryCodeError extends ForbiddenError {
	constructor(hint?: string) {
		super('Invalid MFA recovery code', hint);
	}
}
