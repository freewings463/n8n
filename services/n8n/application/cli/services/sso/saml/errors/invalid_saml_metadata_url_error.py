"""
MIGRATION-META:
  source_path: packages/cli/src/sso.ee/saml/errors/invalid-saml-metadata-url.error.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/sso.ee/saml/errors 的SSO错误。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:InvalidSamlMetadataUrlError。关键函数/方法:无。用于承载SSO实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - SSO integration orchestration -> application/services/sso
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/sso.ee/saml/errors/invalid-saml-metadata-url.error.ts -> services/n8n/application/cli/services/sso/saml/errors/invalid_saml_metadata_url_error.py

import { UserError } from 'n8n-workflow';

export class InvalidSamlMetadataUrlError extends UserError {
	constructor(url: string) {
		super(`Failed to produce valid SAML metadata from ${url}`);
	}
}
