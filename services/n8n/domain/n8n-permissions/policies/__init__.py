"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/src/index.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions/src 的入口。导入/依赖:外部:无；内部:无；本地:无。再导出:./types.ee、./constants.ee、../scopes/global-scopes.ee、./scope-information 等3项。导出:hasScope、hasGlobalScope、combineScopes、staticRolesWithScope、getGlobalScopes、getRoleScopes、getAuthPrincipalScopes、getResourcePermissions。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/src/index.ts -> services/n8n/domain/n8n-permissions/policies/__init__.py

export * from './types.ee';
export * from './constants.ee';

export * from './roles/scopes/global-scopes.ee';
export * from './scope-information';
export * from './roles/role-maps.ee';
export * from './roles/all-roles';

export {
	systemProjectRoleSchema,
	assignableProjectRoleSchema,
	assignableGlobalRoleSchema,
	projectRoleSchema,
	teamRoleSchema,
	roleSchema,
	type Role,
	scopeSchema,
} from './schemas.ee';

export { hasScope } from './utilities/has-scope.ee';
export { hasGlobalScope } from './utilities/has-global-scope.ee';
export { combineScopes } from './utilities/combine-scopes.ee';
export { staticRolesWithScope } from './utilities/static-roles-with-scope.ee';
export { getGlobalScopes } from './utilities/get-global-scopes.ee';
export { getRoleScopes, getAuthPrincipalScopes } from './utilities/get-role-scopes.ee';
export { getResourcePermissions } from './utilities/get-resource-permissions.ee';
export type { PermissionsRecord } from './utilities/get-resource-permissions.ee';
export * from './public-api-permissions.ee';
