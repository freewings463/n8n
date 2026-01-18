"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/configs/version-notifications.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/configs 的配置。导入/依赖:外部:无；内部:无；本地:../decorators。导出:VersionNotificationsConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/configs/version-notifications.config.ts -> services/n8n/infrastructure/n8n-config/configuration/configs/version_notifications_config.py

import { Config, Env } from '../decorators';

@Config
export class VersionNotificationsConfig {
	/** Whether to request notifications about new n8n versions */
	@Env('N8N_VERSION_NOTIFICATIONS_ENABLED')
	enabled: boolean = true;

	/** Endpoint to retrieve n8n version information from */
	@Env('N8N_VERSION_NOTIFICATIONS_ENDPOINT')
	endpoint: string = 'https://api.n8n.io/api/versions/';

	/** Whether to request What's New articles. Also requires `N8N_VERSION_NOTIFICATIONS_ENABLED` to be enabled */
	@Env('N8N_VERSION_NOTIFICATIONS_WHATS_NEW_ENABLED')
	whatsNewEnabled: boolean = true;

	/** Endpoint to retrieve "What's New" articles from */
	@Env('N8N_VERSION_NOTIFICATIONS_WHATS_NEW_ENDPOINT')
	whatsNewEndpoint: string = 'https://api.n8n.io/api/whats-new';

	/** URL for versions panel to page instructing user on how to update n8n instance */
	@Env('N8N_VERSION_NOTIFICATIONS_INFO_URL')
	infoUrl: string = 'https://docs.n8n.io/hosting/installation/updating/';
}
