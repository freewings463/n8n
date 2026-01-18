"""
MIGRATION-META:
  source_path: packages/cli/src/push/push.config.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/push 的配置。导入/依赖:外部:无；内部:@n8n/config；本地:无。导出:PushConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - SSE/WebSocket push adapter -> presentation/api/push
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/push/push.config.ts -> services/n8n/presentation/cli/api/push/push_config.py

import { Config, Env } from '@n8n/config';

@Config
export class PushConfig {
	/** Backend to use for push notifications */
	@Env('N8N_PUSH_BACKEND')
	backend: 'sse' | 'websocket' = 'websocket';
}
