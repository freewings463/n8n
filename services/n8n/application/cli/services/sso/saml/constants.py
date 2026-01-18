"""
MIGRATION-META:
  source_path: packages/cli/src/sso.ee/saml/constants.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/sso.ee/saml 的SSO模块。导入/依赖:外部:无；内部:无；本地:无。导出:SAML_PREFERENCES_DB_KEY、SAML_LOGIN_LABEL、SAML_LOGIN_ENABLED。关键函数/方法:无。用于承载SSO实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - SSO integration orchestration -> application/services/sso
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/sso.ee/saml/constants.ts -> services/n8n/application/cli/services/sso/saml/constants.py

export const SAML_PREFERENCES_DB_KEY = 'features.saml';
export const SAML_LOGIN_LABEL = 'sso.saml.loginLabel';
export const SAML_LOGIN_ENABLED = 'sso.saml.loginEnabled';
