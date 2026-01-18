"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/configs/event-bus.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/configs 的配置。导入/依赖:外部:zod；内部:无；本地:../decorators。导出:EventBusConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/configs/event-bus.config.ts -> services/n8n/infrastructure/n8n-config/configuration/configs/event_bus_config.py

import { z } from 'zod';

import { Config, Env, Nested } from '../decorators';

@Config
class LogWriterConfig {
	/* of event log files to keep */
	@Env('N8N_EVENTBUS_LOGWRITER_KEEPLOGCOUNT')
	keepLogCount: number = 3;

	/** Max size (in KB) of an event log file before a new one is started */
	@Env('N8N_EVENTBUS_LOGWRITER_MAXFILESIZEINKB')
	maxFileSizeInKB: number = 10240; // 10 MB

	/** Basename of event log file */
	@Env('N8N_EVENTBUS_LOGWRITER_LOGBASENAME')
	logBaseName: string = 'n8nEventLog';
}

const recoveryModeSchema = z.enum(['simple', 'extensive']);
type RecoveryMode = z.infer<typeof recoveryModeSchema>;

@Config
export class EventBusConfig {
	/** How often (in ms) to check for unsent event messages. Can in rare cases cause a message to be sent twice. `0` to disable */
	@Env('N8N_EVENTBUS_CHECKUNSENTINTERVAL')
	checkUnsentInterval: number = 0;

	/** Endpoint to retrieve n8n version information from */
	@Nested
	logWriter: LogWriterConfig;

	/** Whether to recover execution details after a crash or only mark status executions as crashed. */
	@Env('N8N_EVENTBUS_RECOVERY_MODE', recoveryModeSchema)
	crashRecoveryMode: RecoveryMode = 'extensive';
}
