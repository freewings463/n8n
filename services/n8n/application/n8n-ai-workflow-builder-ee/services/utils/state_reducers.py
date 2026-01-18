"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/utils/state-reducers.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/utils 的工作流工具。导入/依赖:外部:无；内部:无；本地:../types。导出:appendArrayReducer、cachedTemplatesReducer。关键函数/方法:cachedTemplatesReducer。用于提供工作流通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/utils/state-reducers.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/utils/state_reducers.py

import type { WorkflowMetadata } from '../types';

/**
 * Reducer for appending arrays with null/empty check.
 * Only appends if the update is a non-empty array.
 */
export function appendArrayReducer<T>(current: T[], update: T[] | undefined | null): T[] {
	return update && update.length > 0 ? [...current, ...update] : current;
}

/**
 * Reducer for caching workflow templates, deduplicating by template ID.
 * Merges new templates with existing ones, avoiding duplicates.
 */
export function cachedTemplatesReducer(
	current: WorkflowMetadata[],
	update: WorkflowMetadata[] | undefined | null,
): WorkflowMetadata[] {
	if (!update || update.length === 0) {
		return current;
	}

	// Build a map of existing templates by ID for fast lookup
	const existingById = new Map(current.map((wf) => [wf.templateId, wf]));

	// Add new templates that don't already exist
	for (const workflow of update) {
		if (!existingById.has(workflow.templateId)) {
			existingById.set(workflow.templateId, workflow);
		}
	}

	return Array.from(existingById.values());
}
