"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/configs/dynamic-banners.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/configs 的配置。导入/依赖:外部:无；内部:无；本地:../decorators。导出:DynamicBannersConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/configs/dynamic-banners.config.ts -> services/n8n/infrastructure/n8n-config/configuration/configs/dynamic_banners_config.py

import { Config, Env } from '../decorators';

@Config
export class DynamicBannersConfig {
	@Env('N8N_DYNAMIC_BANNERS_ENDPOINT')
	endpoint: string = 'https://api.n8n.io/api/banners';

	@Env('N8N_DYNAMIC_BANNERS_ENABLED')
	enabled: boolean = true;
}
