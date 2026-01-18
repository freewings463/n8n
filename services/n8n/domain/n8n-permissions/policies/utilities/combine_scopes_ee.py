"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/src/utilities/combine-scopes.ee.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions/src/utilities 的模块。导入/依赖:外部:无；内部:无；本地:../types.ee。导出:combineScopes。关键函数/方法:combineScopes。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/src/utilities/combine-scopes.ee.ts -> services/n8n/domain/n8n-permissions/policies/utilities/combine_scopes_ee.py

import type { Scope, ScopeLevels, MaskLevels } from '../types.ee';

/**
 * Combines scopes from different levels into a deduplicated set.
 *
 * @param userScopes - Scopes organized by level (global, project, resource)
 * @param masks - Optional filters for non-global scopes
 * @returns Set containing all allowed scopes
 *
 * @example
 * combineScopes({
 *   global: ['user:list'],
 *   project: ['workflow:read'],
 * }, { sharing: ['workflow:read'] });
 */
export function combineScopes(userScopes: ScopeLevels, masks?: MaskLevels): Set<Scope> {
	const maskedScopes: ScopeLevels = Object.fromEntries(
		Object.entries(userScopes).map((e) => [e[0], [...e[1]]]),
	) as ScopeLevels;

	if (masks?.sharing) {
		if (maskedScopes.project) {
			maskedScopes.project = maskedScopes.project.filter((v) => masks.sharing.includes(v));
		}
		if (maskedScopes.resource) {
			maskedScopes.resource = maskedScopes.resource.filter((v) => masks.sharing.includes(v));
		}
	}

	return new Set(Object.values(maskedScopes).flat());
}
