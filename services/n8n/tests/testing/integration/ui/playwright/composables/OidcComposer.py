"""
MIGRATION-META:
  source_path: packages/testing/playwright/composables/OidcComposer.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/composables 的组合式函数。导入/依赖:外部:无；内部:无；本地:../pages/n8nPage。导出:OidcComposer。关键函数/方法:configureOidc。用于封装该模块复用逻辑（hooks/composables）供组件组合。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/composables/OidcComposer.ts -> services/n8n/tests/testing/integration/ui/playwright/composables/OidcComposer.py

import type { n8nPage } from '../pages/n8nPage';

/**
 * Composer for OIDC-related operations in E2E tests.
 * Handles configuring OIDC settings.
 */
export class OidcComposer {
	constructor(private readonly n8n: n8nPage) {}

	/**
	 * Configure OIDC via UI form.
	 *
	 * @param discoveryUrl - The discovery URL for n8n backend (e.g., https://keycloak:8443/...)
	 * @param clientId - The OIDC client ID
	 * @param clientSecret - The OIDC client secret
	 */
	async configureOidc(discoveryUrl: string, clientId: string, clientSecret: string): Promise<void> {
		const { settingsSso } = this.n8n;

		await settingsSso.goto();
		await settingsSso.selectOidcProtocol();
		await settingsSso.fillOidcForm({
			discoveryEndpoint: discoveryUrl,
			clientId,
			clientSecret,
			enableLogin: true,
		});
		await settingsSso.saveOidcConfig();
	}
}
