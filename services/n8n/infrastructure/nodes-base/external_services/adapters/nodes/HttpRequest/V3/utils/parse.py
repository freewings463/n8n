"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/HttpRequest/V3/utils/parse.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/HttpRequest/V3 的工具。导入/依赖:外部:无；内部:无；本地:无。导出:mimeTypeFromResponse。关键函数/方法:mimeTypeFromResponse。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/HttpRequest/V3/utils/parse.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/HttpRequest/V3/utils/parse.py

export const mimeTypeFromResponse = (
	responseContentType: string | undefined,
): string | undefined => {
	if (!responseContentType) {
		return undefined;
	}

	return responseContentType.split(' ')[0].split(';')[0];
};
