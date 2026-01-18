"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/src/public-api-permissions.ee.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions/src 的模块。导入/依赖:外部:无；内部:无；本地:./types.ee。导出:OWNER_API_KEY_SCOPES、ADMIN_API_KEY_SCOPES、MEMBER_API_KEY_SCOPES、CHAT_USER_API_KEY_SCOPES、API_KEY_SCOPES_FOR_IMPLICIT_PERSONAL_PROJECT、getApiKeyScopesForRole、getOwnerOnlyApiKeyScopes。关键函数/方法:getApiKeyScopesForRole、getOwnerOnlyApiKeyScopes。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/src/public-api-permissions.ee.ts -> services/n8n/domain/n8n-permissions/policies/public_api_permissions_ee.py

import { isApiKeyScope, type ApiKeyScope, type AuthPrincipal, type GlobalRole } from './types.ee';

export const OWNER_API_KEY_SCOPES: ApiKeyScope[] = [
	'user:read',
	'user:list',
	'user:create',
	'user:changeRole',
	'user:delete',
	'user:enforceMfa',
	'sourceControl:pull',
	'securityAudit:generate',
	'project:create',
	'project:update',
	'project:delete',
	'project:list',
	'variable:create',
	'variable:delete',
	'variable:list',
	'variable:update',
	'tag:create',
	'tag:read',
	'tag:update',
	'tag:delete',
	'tag:list',
	'workflowTags:update',
	'workflowTags:list',
	'workflow:create',
	'workflow:read',
	'workflow:update',
	'workflow:delete',
	'workflow:list',
	'workflow:move',
	'workflow:activate',
	'workflow:deactivate',
	'execution:delete',
	'execution:read',
	'execution:retry',
	'execution:list',
	'credential:create',
	'credential:update',
	'credential:move',
	'credential:delete',
];

export const ADMIN_API_KEY_SCOPES: ApiKeyScope[] = OWNER_API_KEY_SCOPES;

export const MEMBER_API_KEY_SCOPES: ApiKeyScope[] = [
	'tag:create',
	'tag:read',
	'tag:update',
	'tag:list',
	'workflowTags:update',
	'workflowTags:list',
	'workflow:create',
	'workflow:read',
	'workflow:update',
	'workflow:delete',
	'workflow:list',
	'workflow:move',
	'workflow:activate',
	'workflow:deactivate',
	'execution:delete',
	'execution:read',
	'execution:retry',
	'execution:list',
	'credential:create',
	'credential:update',
	'credential:move',
	'credential:delete',
];

export const CHAT_USER_API_KEY_SCOPES: ApiKeyScope[] = [];

/**
 * This is a bit of a mess, because we are handing out scopes in API keys that are only
 * valid for the personal project, which is enforced in the public API, because the workflows,
 * execution endpoints are limited to the personal project.
 * This is a temporary solution until we have a better way to handle personal projects and API key scopes!
 */
export const API_KEY_SCOPES_FOR_IMPLICIT_PERSONAL_PROJECT: ApiKeyScope[] = [
	'workflowTags:update',
	'workflowTags:list',
	'workflow:create',
	'workflow:read',
	'workflow:update',
	'workflow:delete',
	'workflow:list',
	'workflow:move',
	'workflow:activate',
	'workflow:deactivate',
	'execution:delete',
	'execution:read',
	'execution:retry',
	'execution:list',
	'credential:create',
	'credential:update',
	'credential:move',
	'credential:delete',
];

const MAP_ROLE_SCOPES: Record<GlobalRole, ApiKeyScope[]> = {
	'global:owner': OWNER_API_KEY_SCOPES,
	'global:admin': ADMIN_API_KEY_SCOPES,
	'global:member': MEMBER_API_KEY_SCOPES,
	'global:chatUser': CHAT_USER_API_KEY_SCOPES,
};

export const getApiKeyScopesForRole = (user: AuthPrincipal) => {
	if (user.role.slug === 'global:chatUser') {
		return [];
	}

	return [
		...new Set(
			user.role.scopes
				.map((scope) => scope.slug)
				.concat(API_KEY_SCOPES_FOR_IMPLICIT_PERSONAL_PROJECT)
				.filter(isApiKeyScope),
		),
	];
};

export const getOwnerOnlyApiKeyScopes = () => {
	const ownerScopes = new Set<ApiKeyScope>(MAP_ROLE_SCOPES['global:owner']);
	const memberScopes = new Set<ApiKeyScope>(MAP_ROLE_SCOPES['global:member']);
	memberScopes.forEach((item) => ownerScopes.delete(item));
	return Array.from(ownerScopes);
};
