"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/src/utilities/get-global-scopes.ee.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions/src/utilities 的模块。导入/依赖:外部:无；内部:无；本地:../types.ee。导出:getGlobalScopes。关键函数/方法:getGlobalScopes。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/src/utilities/get-global-scopes.ee.ts -> services/n8n/domain/n8n-permissions/policies/utilities/get_global_scopes_ee.py

import type { AuthPrincipal } from '../types.ee';

/**
 * Gets global scopes for a principal's role.
 * @param principal - Contains the role to look up
 * @returns Array of scopes for the role, or empty array if not found
 */
export const getGlobalScopes = (principal: AuthPrincipal) =>
	principal.role.scopes.map((scope) => scope.slug) ?? [];
