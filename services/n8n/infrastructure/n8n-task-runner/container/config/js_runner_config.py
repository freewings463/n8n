"""
MIGRATION-META:
  source_path: packages/@n8n/task-runner/src/config/js-runner-config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/task-runner/src/config 的配置。导入/依赖:外部:无；内部:@n8n/config；本地:无。导出:JsRunnerConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Task runner process runtime -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/task-runner/src/config/js-runner-config.ts -> services/n8n/infrastructure/n8n-task-runner/container/config/js_runner_config.py

import { Config, Env } from '@n8n/config';

@Config
export class JsRunnerConfig {
	@Env('NODE_FUNCTION_ALLOW_BUILTIN')
	allowedBuiltInModules: string = '';

	@Env('NODE_FUNCTION_ALLOW_EXTERNAL')
	allowedExternalModules: string = '';

	@Env('N8N_RUNNERS_INSECURE_MODE')
	insecureMode: boolean = false;
}
