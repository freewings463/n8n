"""
MIGRATION-META:
  source_path: packages/@n8n/config/src/configs/generic.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/config/src/configs 的配置。导入/依赖:外部:zod；内部:无；本地:../decorators。导出:GenericConfig。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/config treated as infrastructure configuration/runtime environment
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/config/src/configs/generic.config.ts -> services/n8n/infrastructure/n8n-config/configuration/configs/generic_config.py

import { z } from 'zod';

import { Config, Env } from '../decorators';

const releaseChannelSchema = z.enum(['stable', 'beta', 'nightly', 'dev', 'rc']);
type ReleaseChannel = z.infer<typeof releaseChannelSchema>;

@Config
export class GenericConfig {
	/** Default timezone for the n8n instance. Can be overridden on a per-workflow basis. */
	@Env('GENERIC_TIMEZONE')
	timezone: string = 'America/New_York';

	@Env('N8N_RELEASE_TYPE', releaseChannelSchema)
	releaseChannel: ReleaseChannel = 'dev';

	/** Grace period (in seconds) to wait for components to shut down before process exit. */
	@Env('N8N_GRACEFUL_SHUTDOWN_TIMEOUT')
	gracefulShutdownTimeout: number = 30;
}
