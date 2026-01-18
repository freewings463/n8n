"""
MIGRATION-META:
  source_path: packages/workflow/src/node-parameters/path-utils.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/node-parameters 的工作流模块。导入/依赖:外部:无；内部:无；本地:无。导出:resolveRelativePath。关键函数/方法:resolveRelativePath。用于承载工作流实现细节，并通过导出对外提供能力。注释目标:Resolve relative paths starting in & in the context of a given full path including parameters, / which will be dropped in the process.。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/node-parameters/path-utils.ts -> services/n8n/domain/workflow/services/node-parameters/path_utils.py

/**
 * Resolve relative paths starting in & in the context of a given full path including parameters,
 * which will be dropped in the process.
 * If `candidateRelativePath` is not relative, it is returned unchanged.
 *
 * `parameters.a.b.c`, `&d` -> `a.b.d`
 * `parameters.a.b[0].c`, `&d` -> `a.b[0].d`
 * `parameters.a.b.c`, `d` -> `d`
 */
export function resolveRelativePath(
	fullPathWithParameters: string,
	candidateRelativePath: string,
): string {
	if (candidateRelativePath.startsWith('&')) {
		const resolvedLeaf = candidateRelativePath.slice(1);
		const pathToLeaf = fullPathWithParameters.split('.').slice(1, -1).join('.');

		if (!pathToLeaf) return resolvedLeaf;

		return `${pathToLeaf}.${resolvedLeaf}`;
	}

	return candidateRelativePath;
}
