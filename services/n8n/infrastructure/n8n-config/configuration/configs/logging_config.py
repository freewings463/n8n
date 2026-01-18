"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/configs/logging.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/configs 的配置。导入/依赖:外部:zod；内部:无；本地:../custom-types、../decorators。导出:LOG_SCOPES、LogScope、CronLoggingConfig、LoggingConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/configs/logging.config.ts -> services/n8n/infrastructure/n8n-config/configuration/configs/logging_config.py

import { z } from 'zod';

import { CommaSeparatedStringArray } from '../custom-types';
import { Config, Env, Nested } from '../decorators';

/** Scopes (areas of functionality) to filter logs by. */
export const LOG_SCOPES = [
	'concurrency',
	'external-secrets',
	'license',
	'multi-main-setup',
	'pruning',
	'pubsub',
	'push',
	'redis',
	'scaling',
	'waiting-executions',
	'task-runner',
	'task-runner-js',
	'task-runner-py',
	'insights',
	'workflow-activation',
	'ssh-client',
	'data-table',
	'cron',
	'community-nodes',
	'legacy-sqlite-execution-recovery',
	'chat-hub',
	'breaking-changes',
	'circuit-breaker',
	'source-control',
	'dynamic-credentials',
	'workflow-history-compaction',
] as const;

export type LogScope = (typeof LOG_SCOPES)[number];

@Config
export class CronLoggingConfig {
	/**
	 * Interval in minutes to log currently active cron jobs. Set to `0` to disable.
	 *
	 * @example `N8N_LOG_CRON_ACTIVE_INTERVAL=30` will log active crons every 30 minutes.
	 */
	@Env('N8N_LOG_CRON_ACTIVE_INTERVAL')
	activeInterval: number = 0;
}

@Config
class FileLoggingConfig {
	/**
	 * Max number of log files to keep, or max number of days to keep logs for.
	 * Once the limit is reached, the oldest log files will be rotated out.
	 * If using days, append a `d` suffix. Only for `file` log output.
	 *
	 * @example `N8N_LOG_FILE_COUNT_MAX=7` will keep at most 7 files.
	 * @example `N8N_LOG_FILE_COUNT_MAX=7d` will keep at most 7 days worth of files.
	 */
	@Env('N8N_LOG_FILE_COUNT_MAX')
	fileCountMax: number = 100;

	/** Max size (in MiB) for each log file. Only for `file` log output. */
	@Env('N8N_LOG_FILE_SIZE_MAX')
	fileSizeMax: number = 16;

	/** Location of the log files inside `~/.n8n`. Only for `file` log output. */
	@Env('N8N_LOG_FILE_LOCATION')
	location: string = 'logs/n8n.log';
}

const logLevelSchema = z.enum(['error', 'warn', 'info', 'debug', 'silent']);
type LogLevel = z.infer<typeof logLevelSchema>;

@Config
export class LoggingConfig {
	/**
	 * Minimum level of logs to output. Logs with this or higher level will be output;
	 * logs with lower levels will not. Exception: `silent` disables all logging.
	 *
	 * @example `N8N_LOG_LEVEL=info` will output `error`, `warn` and `info` logs, but not `debug`.
	 */
	@Env('N8N_LOG_LEVEL', logLevelSchema)
	level: LogLevel = 'info';

	/**
	 * Where to output logs to. Options are: `console` or `file` or both in a comma separated list.
	 *
	 * @example `N8N_LOG_OUTPUT=console,file` will output to both console and file.
	 */
	@Env('N8N_LOG_OUTPUT')
	outputs: CommaSeparatedStringArray<'console' | 'file'> = ['console'];

	/**
	 * What format the logs should have.
	 * `text` is only printing the human readable messages.
	 * `json` is printing one JSON object per line containing the message, level,
	 * timestamp and all the metadata.
	 */
	@Env('N8N_LOG_FORMAT')
	format: 'text' | 'json' = 'text';

	@Nested
	file: FileLoggingConfig;

	@Nested
	cron: CronLoggingConfig;

	/**
	 * Scopes to filter logs by. Nothing is filtered by default.
	 *
	 * Supported log scopes:
	 *
	 * - `concurrency`
	 * - `external-secrets`
	 * - `license`
	 * - `multi-main-setup`
	 * - `pruning`
	 * - `pubsub`
	 * - `push`
	 * - `redis`
	 * - `scaling`
	 * - `waiting-executions`
	 * - `task-runner-js`
	 * - `task-runner-py`
	 * - `workflow-activation`
	 * - `insights`
	 * - `chat-hub`
	 *
	 * @example
	 * `N8N_LOG_SCOPES=license`
	 * `N8N_LOG_SCOPES=license,waiting-executions`
	 */
	@Env('N8N_LOG_SCOPES')
	scopes: CommaSeparatedStringArray<LogScope> = [];
}
