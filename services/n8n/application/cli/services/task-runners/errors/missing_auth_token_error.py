"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/errors/missing-auth-token.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/task-runners/errors 的错误。导入/依赖:外部:无；内部:无；本地:无。导出:MissingAuthTokenError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/errors/missing-auth-token.error.ts -> services/n8n/application/cli/services/task-runners/errors/missing_auth_token_error.py

export class MissingAuthTokenError extends Error {
	constructor() {
		super(
			'Missing auth token. When `N8N_RUNNERS_MODE` is `external`, it is required to set `N8N_RUNNERS_AUTH_TOKEN`. Its value should be a shared secret between the main instance and the launcher.',
		);
	}
}
