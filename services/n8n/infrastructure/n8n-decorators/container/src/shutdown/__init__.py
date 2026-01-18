"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/shutdown/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src/shutdown 的入口。导入/依赖:外部:无；内部:无；本地:无。导出:ShutdownMetadata、OnShutdown。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/shutdown/index.ts -> services/n8n/infrastructure/n8n-decorators/container/src/shutdown/__init__.py

export {
	HIGHEST_SHUTDOWN_PRIORITY,
	DEFAULT_SHUTDOWN_PRIORITY,
	LOWEST_SHUTDOWN_PRIORITY,
} from './constants';
export { ShutdownMetadata } from './shutdown-metadata';
export { OnShutdown } from './on-shutdown';
export type { ShutdownHandler, ShutdownServiceClass } from './types';
