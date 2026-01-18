"""
MIGRATION-META:
  source_path: packages/cli/src/sso.ee/saml/types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/sso.ee/saml 的SSO类型。导入/依赖:外部:无；内部:@n8n/api-types；本地:无。导出:SamlLoginBinding、SamlAttributeMapping、SamlUserAttributes。关键函数/方法:无。用于定义SSO相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - SSO integration orchestration -> application/services/sso
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/sso.ee/saml/types.ts -> services/n8n/application/cli/services/sso/saml/types.py

import type { SamlPreferences, SamlPreferencesAttributeMapping } from '@n8n/api-types';

export type SamlLoginBinding = SamlPreferences['loginBinding'];
export type SamlAttributeMapping = NonNullable<SamlPreferencesAttributeMapping>;
export type SamlUserAttributes = SamlAttributeMapping;
