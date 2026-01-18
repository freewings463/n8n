"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/configs/diagnostics.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/configs 的配置。导入/依赖:外部:无；内部:无；本地:../decorators。导出:DiagnosticsConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/configs/diagnostics.config.ts -> services/n8n/infrastructure/n8n-config/configuration/configs/diagnostics_config.py

import { Config, Env, Nested } from '../decorators';

@Config
class PostHogConfig {
	/** API key for PostHog. */
	@Env('N8N_DIAGNOSTICS_POSTHOG_API_KEY')
	apiKey: string = 'phc_4URIAm1uYfJO7j8kWSe0J8lc8IqnstRLS7Jx8NcakHo';

	/** API host for PostHog. */
	@Env('N8N_DIAGNOSTICS_POSTHOG_API_HOST')
	apiHost: string = 'https://us.i.posthog.com';
}

@Config
export class DiagnosticsConfig {
	/** Whether diagnostics are enabled. */
	@Env('N8N_DIAGNOSTICS_ENABLED')
	enabled: boolean = true;

	/** Diagnostics config for frontend. */
	@Env('N8N_DIAGNOSTICS_CONFIG_FRONTEND')
	frontendConfig: string = '1zPn9bgWPzlQc0p8Gj1uiK6DOTn;https://telemetry.n8n.io';

	/** Diagnostics config for backend. */
	@Env('N8N_DIAGNOSTICS_CONFIG_BACKEND')
	backendConfig: string = '1zPn7YoGC3ZXE9zLeTKLuQCB4F6;https://telemetry.n8n.io';

	@Nested
	posthogConfig: PostHogConfig;
}
