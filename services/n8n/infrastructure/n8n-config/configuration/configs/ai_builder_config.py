"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/configs/ai-builder.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/configs 的配置。导入/依赖:外部:无；内部:无；本地:../decorators。导出:AiBuilderConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/configs/ai-builder.config.ts -> services/n8n/infrastructure/n8n-config/configuration/configs/ai_builder_config.py

import { Config, Env } from '../decorators';

@Config
export class AiBuilderConfig {
	/** Keys for local service */
	@Env('N8N_AI_ANTHROPIC_KEY')
	apiKey: string = '';
}
