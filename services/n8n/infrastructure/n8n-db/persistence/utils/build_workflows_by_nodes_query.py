"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/utils/build-workflows-by-nodes-query.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/utils 的工作流工具。导入/依赖:外部:无；内部:无；本地:无。导出:buildWorkflowsByNodesQuery。关键函数/方法:buildWorkflowsByNodesQuery。用于提供工作流通用工具能力（纯函数/封装器）供复用。注释目标:Builds the WHERE clause and parameters for a query to find workflows by node types。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package @n8n/db defaulted to persistence infrastructure
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/utils/build-workflows-by-nodes-query.ts -> services/n8n/infrastructure/n8n-db/persistence/utils/build_workflows_by_nodes_query.py

/**
 * Builds the WHERE clause and parameters for a query to find workflows by node types
 */
export function buildWorkflowsByNodesQuery(
	nodeTypes: string[],
	dbType: 'postgresdb' | 'mysqldb' | 'mariadb' | 'sqlite',
) {
	let whereClause: string;

	const parameters: Record<string, string | string[]> = { nodeTypes };

	switch (dbType) {
		case 'postgresdb':
			whereClause = `EXISTS (
					SELECT 1
					FROM jsonb_array_elements(workflow.nodes::jsonb) AS node
					WHERE node->>'type' = ANY(:nodeTypes)
				)`;
			break;
		case 'mysqldb':
		case 'mariadb': {
			const conditions = nodeTypes
				.map(
					(_, i) =>
						`JSON_SEARCH(JSON_EXTRACT(workflow.nodes, '$[*].type'), 'one', :nodeType${i}) IS NOT NULL`,
				)
				.join(' OR ');

			whereClause = `(${conditions})`;

			nodeTypes.forEach((nodeType, index) => {
				parameters[`nodeType${index}`] = nodeType;
			});
			break;
		}
		case 'sqlite': {
			const conditions = nodeTypes
				.map(
					(_, i) =>
						`EXISTS (SELECT 1 FROM json_each(workflow.nodes) WHERE json_extract(json_each.value, '$.type') = :nodeType${i})`,
				)
				.join(' OR ');

			whereClause = `(${conditions})`;

			nodeTypes.forEach((nodeType, index) => {
				parameters[`nodeType${index}`] = nodeType;
			});
			break;
		}
		default:
			throw new Error('Unsupported database type');
	}

	return { whereClause, parameters };
}
