"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/validation/utils/is-tool.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/validation/utils 的工作流工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:isTool。关键函数/方法:isTool。用于提供工作流通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/validation/utils/is-tool.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/validation/utils/is_tool.py

import type { INodeTypeDescription } from 'n8n-workflow';

export function isTool(nodeType: INodeTypeDescription): boolean {
	return nodeType.codex?.subcategories?.AI?.includes('Tools') ?? false;
}
