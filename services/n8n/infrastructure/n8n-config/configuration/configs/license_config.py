"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/configs/license.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/configs 的配置。导入/依赖:外部:无；内部:无；本地:../decorators。导出:LicenseConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/configs/license.config.ts -> services/n8n/infrastructure/n8n-config/configuration/configs/license_config.py

import { Config, Env } from '../decorators';

@Config
export class LicenseConfig {
	/** License server URL to retrieve license. */
	@Env('N8N_LICENSE_SERVER_URL')
	serverUrl: string = 'https://license.n8n.io/v1';

	/** Whether autorenewal for licenses is enabled. */
	@Env('N8N_LICENSE_AUTO_RENEW_ENABLED')
	autoRenewalEnabled: boolean = true;

	/** Activation key to initialize license. */
	@Env('N8N_LICENSE_ACTIVATION_KEY')
	activationKey: string = '';

	/** Whether floating entitlements should be returned to the pool on shutdown */
	@Env('N8N_LICENSE_DETACH_FLOATING_ON_SHUTDOWN')
	detachFloatingOnShutdown: boolean = true;

	/** Tenant ID used by the license manager SDK, e.g. for self-hosted, sandbox, embed, cloud. */
	@Env('N8N_LICENSE_TENANT_ID')
	tenantId: number = 1;

	/** Ephemeral license certificate. See: https://github.com/n8n-io/license-management?tab=readme-ov-file#concept-ephemeral-entitlements */
	@Env('N8N_LICENSE_CERT')
	cert: string = '';
}
