"""
MIGRATION-META:
  source_path: packages/cli/src/config/schema.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/config 的配置。导入/依赖:外部:无；内部:@n8n/config、@n8n/di；本地:无。导出:schema。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/config/schema.ts -> services/n8n/application/cli/services/config/schema.py

import { GlobalConfig } from '@n8n/config';
import { Container } from '@n8n/di';

/**
 * @deprecated Do not add new environment variables to this file. Please use the `@n8n/config` package instead.
 */
export const schema = {
	userManagement: {
		/**
		 * @important Do not remove isInstanceOwnerSetUp until after cloud hooks (user-management) are updated to stop using
		 * this property
		 * @deprecated
		 */
		isInstanceOwnerSetUp: {
			// n8n loads this setting from SettingsRepository (DB) on startup
			doc: "Whether the instance owner's account has been set up",
			format: Boolean,
			default: false,
		},

		/**
		 * @techdebt Refactor this to stop using the legacy config schema for internal state.
		 */
		authenticationMethod: {
			doc: 'How to authenticate users (e.g. "email", "ldap", "saml")',
			format: ['email', 'ldap', 'saml'] as const,
			default: 'email',
		},
	},

	/**
	 * @important Do not remove until after cloud hooks are updated to stop using convict config.
	 */
	endpoints: {
		rest: {
			format: String,
			default: Container.get(GlobalConfig).endpoints.rest,
		},
	},

	/**
	 * @important Do not remove until after cloud hooks are updated to stop using convict config.
	 */
	ai: {
		enabled: {
			format: Boolean,
			default: Container.get(GlobalConfig).ai.enabled,
		},
	},
};
