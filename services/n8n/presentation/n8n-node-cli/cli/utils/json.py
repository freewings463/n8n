"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/utils/json.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/node-cli/src/utils 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:jsonParse。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI package default -> presentation/cli
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/utils/json.ts -> services/n8n/presentation/n8n-node-cli/cli/utils/json.py

export function jsonParse<T>(data: string): T | null {
	try {
		return JSON.parse(data) as T;
	} catch (error) {
		return null;
	}
}
