"""
MIGRATION-META:
  source_path: packages/@n8n/task-runner/src/config/main-config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/task-runner/src/config 的配置。导入/依赖:外部:无；内部:@n8n/config；本地:./base-runner-config、./js-runner-config、./sentry-config。导出:MainConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Task runner process runtime -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/task-runner/src/config/main-config.ts -> services/n8n/infrastructure/n8n-task-runner/container/config/main_config.py

import { Config, Nested } from '@n8n/config';

import { BaseRunnerConfig } from './base-runner-config';
import { JsRunnerConfig } from './js-runner-config';
import { SentryConfig } from './sentry-config';

@Config
export class MainConfig {
	@Nested
	baseRunnerConfig!: BaseRunnerConfig;

	@Nested
	jsRunnerConfig!: JsRunnerConfig;

	@Nested
	sentryConfig!: SentryConfig;
}
