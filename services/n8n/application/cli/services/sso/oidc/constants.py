"""
MIGRATION-META:
  source_path: packages/cli/src/sso.ee/oidc/constants.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/sso.ee/oidc 的SSO模块。导入/依赖:外部:无；内部:无；本地:无。导出:OIDC_PREFERENCES_DB_KEY、OIDC_LOGIN_ENABLED、OIDC_CLIENT_SECRET_REDACTED_VALUE。关键函数/方法:无。用于承载SSO实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - SSO integration orchestration -> application/services/sso
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/sso.ee/oidc/constants.ts -> services/n8n/application/cli/services/sso/oidc/constants.py

export const OIDC_PREFERENCES_DB_KEY = 'features.oidc';
export const OIDC_LOGIN_ENABLED = 'sso.oidc.loginEnabled';
export const OIDC_CLIENT_SECRET_REDACTED_VALUE =
	'__n8n_CLIENT_SECRET_VALUE_e5362baf-c777-4d57-a609-6eaf1f9e87f6';
