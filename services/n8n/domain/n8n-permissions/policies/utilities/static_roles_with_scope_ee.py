"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/src/utilities/static-roles-with-scope.ee.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions/src/utilities 的模块。导入/依赖:外部:无；内部:无；本地:../roles/role-maps.ee、../types.ee。导出:staticRolesWithScope。关键函数/方法:staticRolesWithScope。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/src/utilities/static-roles-with-scope.ee.ts -> services/n8n/domain/n8n-permissions/policies/utilities/static_roles_with_scope_ee.py

import { ALL_ROLE_MAPS } from '../roles/role-maps.ee';
import type { RoleNamespace, Scope } from '../types.ee';

/**
 * Retrieves roles within a specific namespace that have all the given scopes.
 *
 * This is only valid for static roles defined in ALL_ROLE_MAPS, with custom roles
 * being handled in the RoleService.
 *
 * @param namespace - The role namespace to search in
 * @param scopes - Scope(s) to filter by
 */
export function staticRolesWithScope(namespace: RoleNamespace, scopes: Scope | Scope[]) {
	if (!Array.isArray(scopes)) {
		scopes = [scopes];
	}

	return Object.keys(ALL_ROLE_MAPS[namespace]).filter((k) => {
		return scopes.every((s) =>
			// eslint-disable-next-line @typescript-eslint/no-explicit-any, @typescript-eslint/no-unsafe-member-access
			((ALL_ROLE_MAPS[namespace] as any)[k] as Scope[]).includes(s),
		);
	});
}
