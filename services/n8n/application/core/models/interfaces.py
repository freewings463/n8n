"""
MIGRATION-META:
  source_path: packages/core/src/interfaces.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:Class、IResponseError、IWorkflowSettings、IWorkflowData、ExtendedValidationResult。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core shared interfaces/types -> application/models
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/interfaces.ts -> services/n8n/application/core/models/interfaces.py

import type {
	ITriggerResponse,
	IWorkflowSettings as IWorkflowSettingsWorkflow,
	ValidationResult,
} from 'n8n-workflow';

export type Class<T = object, A extends unknown[] = unknown[]> = new (...args: A) => T;

export interface IResponseError extends Error {
	statusCode?: number;
}

export interface IWorkflowSettings extends IWorkflowSettingsWorkflow {
	errorWorkflow?: string;
	timezone?: string;
	saveManualRuns?: boolean;
}

export interface IWorkflowData {
	triggerResponses?: ITriggerResponse[];
}

export type ExtendedValidationResult = ValidationResult & { fieldName?: string };
