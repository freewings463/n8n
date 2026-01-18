"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/configs/workflow-history-compaction.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/configs 的工作流配置。导入/依赖:外部:无；内部:无；本地:../decorators。导出:WorkflowHistoryCompactionConfig。关键函数/方法:无。用于集中定义工作流配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/configs/workflow-history-compaction.config.ts -> services/n8n/infrastructure/n8n-config/configuration/configs/workflow_history_compaction_config.py

import { Config, Env } from '../decorators';

@Config
export class WorkflowHistoryCompactionConfig {
	@Env('N8N_WORKFLOW_HISTORY_COMPACTION_MINIMUM_AGE_HOURS')
	/**
	 * The minimum time we leave workflows in the history untouched
	 * before we start compacting them.
	 *
	 * The workflow versions we compare and compact are those with
	 * a `createdAt` value between `compactingMinimumAgeHours - compactingTimeWindowHours`
	 * and `compactingMinimumAgeHours`

	 */
	compactingMinimumAgeHours: number = 3;

	/**
	 * The time window we consider when compacting versions.
	 *
	 * The workflow versions we compare and compact are those with
	 * a `createdAt` value between `compactingMinimumAgeHours - compactingTimeWindowHours`
	 * and `compactingMinimumAgeHours`.
	 *
	 * Compaction will happen every `compactingTimeWindowHours/2` hours to
	 * account for small gaps and downtime.
	 */
	@Env('N8N_WORKFLOW_HISTORY_COMPACTION_TIME_WINDOW_HOURS')
	compactingTimeWindowHours: number = 2;

	/**
	 * The maximum number of compared workflow versions before waiting `batchDelayMs`
	 * before continuing with the next workflowId
	 */
	@Env('N8N_WORKFLOW_HISTORY_COMPACTION_BATCH_SIZE')
	batchSize: number = 100;

	/**
	 * Delay in milliseconds before continuing with the next workflowId to compact
	 * after having compared at least `batchSize` workflow versions
	 */
	@Env('N8N_WORKFLOW_HISTORY_COMPACTION_BATCH_DELAY_MS')
	batchDelayMs: number = 1_000;

	/**
	 * Whether to run compaction on instance start up.
	 *
	 * Useful to apply a larger compaction value to cover existing
	 * histories if something went wrong previously, and for development.
	 *
	 * @warning Long-running blocking operation that will increase startup time.
	 */
	@Env('N8N_WORKFLOW_HISTORY_COMPACTION_RUN_ON_START_UP')
	compactOnStartUp: boolean = false;

	/**
	 * The minimum time in milliseconds before two consecutive versions are
	 * considered part of different sessions and should thus never be merged together.
	 */
	@Env('N8N_WORKFLOW_HISTORY_COMPACTION_MINIMUM_TIME_BETWEEN_SESSIONS_MS')
	minimumTimeBetweenSessionsMs: number = 20 * 60 * 1000;
}
