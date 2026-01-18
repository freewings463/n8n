"""
MIGRATION-META:
  source_path: packages/workflow/src/tool-helpers.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src 的工作流工具。导入/依赖:外部:无；内部:无；本地:./interfaces。导出:nodeNameToToolName。关键函数/方法:nodeNameToToolName。用于提供工作流通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/tool-helpers.ts -> services/n8n/domain/workflow/services/tool_helpers.py

import type { INode } from './interfaces';

/**
 * Converts a node name to a valid tool name by replacing special characters with underscores
 * and collapsing consecutive underscores into a single one.
 */
export function nodeNameToToolName(nodeOrName: INode | string): string {
	const name = typeof nodeOrName === 'string' ? nodeOrName : nodeOrName.name;
	return name.replace(/[^a-zA-Z0-9_-]+/g, '_');
}
