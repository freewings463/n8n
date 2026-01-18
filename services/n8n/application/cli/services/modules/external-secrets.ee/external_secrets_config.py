"""
MIGRATION-META:
  source_path: packages/cli/src/modules/external-secrets.ee/external-secrets.config.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/external-secrets.ee 的配置。导入/依赖:外部:无；内部:@n8n/config；本地:无。导出:ExternalSecretsConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/external-secrets.ee/external-secrets.config.ts -> services/n8n/application/cli/services/modules/external-secrets.ee/external_secrets_config.py

import { Config, Env } from '@n8n/config';

@Config
export class ExternalSecretsConfig {
	/** How often (in seconds) to check for secret updates */
	@Env('N8N_EXTERNAL_SECRETS_UPDATE_INTERVAL')
	updateInterval: number = 300;

	/** Whether to prefer GET over LIST when fetching secrets from Hashicorp Vault */
	@Env('N8N_EXTERNAL_SECRETS_PREFER_GET')
	preferGet: boolean = false;
}
