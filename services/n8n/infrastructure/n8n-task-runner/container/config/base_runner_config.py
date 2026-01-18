"""
MIGRATION-META:
  source_path: packages/@n8n/task-runner/src/config/base-runner-config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/task-runner/src/config 的配置。导入/依赖:外部:无；内部:@n8n/config；本地:无。导出:BaseRunnerConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Task runner process runtime -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/task-runner/src/config/base-runner-config.ts -> services/n8n/infrastructure/n8n-task-runner/container/config/base_runner_config.py

import { Config, Env, Nested } from '@n8n/config';

@Config
class HealthcheckServerConfig {
	@Env('N8N_RUNNERS_HEALTH_CHECK_SERVER_ENABLED')
	enabled: boolean = false;

	@Env('N8N_RUNNERS_HEALTH_CHECK_SERVER_HOST')
	host: string = '127.0.0.1';

	@Env('N8N_RUNNERS_HEALTH_CHECK_SERVER_PORT')
	port: number = 5681;
}

@Config
export class BaseRunnerConfig {
	@Env('N8N_RUNNERS_TASK_BROKER_URI')
	taskBrokerUri: string = 'http://127.0.0.1:5679';

	@Env('N8N_RUNNERS_GRANT_TOKEN')
	grantToken: string = '';

	@Env('N8N_RUNNERS_MAX_PAYLOAD')
	maxPayloadSize: number = 1024 * 1024 * 1024;

	/**
	 * How many concurrent tasks can a runner execute at a time
	 *
	 * Kept high for backwards compatibility - n8n v2 will reduce this to `5`
	 */
	@Env('N8N_RUNNERS_MAX_CONCURRENCY')
	maxConcurrency: number = 10;

	/**
	 * How long (in seconds) a runner may be idle for before exit. Intended
	 * for use in `external` mode - launcher must pass the env var when launching
	 * the runner. Disabled with `0` on `internal` mode.
	 */
	@Env('N8N_RUNNERS_AUTO_SHUTDOWN_TIMEOUT')
	idleTimeout: number = 0;

	@Env('GENERIC_TIMEZONE')
	timezone: string = 'America/New_York';

	/**
	 * How long (in seconds) a task is allowed to take for completion, else the
	 * task will be aborted. (In internal mode, the runner will also be
	 * restarted.) Must be greater than 0.
	 *
	 * Kept high for backwards compatibility - n8n v2 will reduce this to `60`
	 */
	@Env('N8N_RUNNERS_TASK_TIMEOUT')
	taskTimeout: number = 300; // 5 minutes

	@Nested
	healthcheckServer!: HealthcheckServerConfig;
}
