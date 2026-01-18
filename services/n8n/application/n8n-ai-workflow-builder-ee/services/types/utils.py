"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/types/utils.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/types 的工作流类型。导入/依赖:外部:无；内部:无；本地:../workflow-state。导出:StateUpdater。关键函数/方法:无。用于定义工作流相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/types/utils.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/types/utils.py

import type { WorkflowState } from '../workflow-state';

/**
 * Type for state updater functions
 */
export type StateUpdater<TState = typeof WorkflowState.State> =
	| Partial<TState>
	| ((state: TState) => Partial<TState>);
