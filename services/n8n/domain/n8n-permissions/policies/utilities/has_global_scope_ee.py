"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/src/utilities/has-global-scope.ee.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions/src/utilities 的模块。导入/依赖:外部:无；内部:无；本地:./has-scope.ee、../types.ee、./get-role-scopes.ee。导出:hasGlobalScope。关键函数/方法:hasGlobalScope。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/src/utilities/has-global-scope.ee.ts -> services/n8n/domain/n8n-permissions/policies/utilities/has_global_scope_ee.py

import { hasScope } from './has-scope.ee';
import type { AuthPrincipal, Scope, ScopeOptions } from '../types.ee';
import { getAuthPrincipalScopes } from './get-role-scopes.ee';

/**
 * Checks if an auth-principal has specified global scope(s).
 * @param principal - The authentication principal to check permissions for
 * @param scope - Scope(s) to verify
 */
export const hasGlobalScope = (
	principal: AuthPrincipal,
	scope: Scope | Scope[],
	scopeOptions?: ScopeOptions,
): boolean => {
	const global = getAuthPrincipalScopes(principal);
	return hasScope(scope, { global }, undefined, scopeOptions);
};
