"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/shutdown/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src/shutdown 的类型。导入/依赖:外部:无；内部:无；本地:../types。导出:ShutdownServiceClass、ShutdownHandler。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/shutdown/types.ts -> services/n8n/infrastructure/n8n-decorators/container/src/shutdown/types.py

import type { Class } from '../types';

type ShutdownHandlerFn = () => Promise<void> | void;
export type ShutdownServiceClass = Class<Record<string, ShutdownHandlerFn>>;

export interface ShutdownHandler {
	serviceClass: ShutdownServiceClass;
	methodName: string;
}
