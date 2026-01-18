"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/src/utilities/has-scope.ee.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions/src/utilities 的模块。导入/依赖:外部:无；内部:无；本地:./combine-scopes.ee、../types.ee。导出:hasScope。关键函数/方法:hasScope。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/src/utilities/has-scope.ee.ts -> services/n8n/domain/n8n-permissions/policies/utilities/has_scope_ee.py

import { combineScopes } from './combine-scopes.ee';
import type { Scope, ScopeLevels, ScopeOptions, MaskLevels } from '../types.ee';

/**
 * Checks if scopes exist in user's permissions.
 * @param scope - Scope(s) to check
 * @param userScopes - User's permission levels
 * @param masks - Optional scope filters
 * @param options - Checking mode (default: oneOf)
 */
export const hasScope = (
	scope: Scope | Scope[],
	userScopes: ScopeLevels,
	masks?: MaskLevels,
	options: ScopeOptions = { mode: 'oneOf' },
): boolean => {
	if (!Array.isArray(scope)) scope = [scope];
	const userScopeSet = combineScopes(userScopes, masks);
	return options.mode === 'allOf'
		? !!scope.length && scope.every((s) => userScopeSet.has(s))
		: scope.some((s) => userScopeSet.has(s));
};
