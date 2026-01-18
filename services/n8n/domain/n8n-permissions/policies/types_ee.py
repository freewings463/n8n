"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/src/types.ee.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions/src 的类型。导入/依赖:外部:zod；内部:无；本地:./constants.ee、./scope-information。导出:ScopeInformation、Resource、Scope、ScopeLevels、MaskLevels、ScopeOptions、RoleNamespace、GlobalRole 等14项。关键函数/方法:isAssignableProjectRoleSlug、isApiKeyScope。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/src/types.ee.ts -> services/n8n/domain/n8n-permissions/policies/types_ee.py

import type { z } from 'zod';

import type { RESOURCES, API_KEY_RESOURCES } from './constants.ee';
import type {
	assignableGlobalRoleSchema,
	credentialSharingRoleSchema,
	globalRoleSchema,
	Role,
	systemProjectRoleSchema,
	roleNamespaceSchema,
	teamRoleSchema,
	workflowSharingRoleSchema,
	assignableProjectRoleSchema,
} from './schemas.ee';
import { PROJECT_OWNER_ROLE_SLUG } from './constants.ee';
import { ALL_API_KEY_SCOPES } from './scope-information';

export type ScopeInformation = {
	displayName: string;
	description?: string | null;
};

/** Represents a resource that can have permissions applied to it */
export type Resource = keyof typeof RESOURCES;

/** A permission scope for a specific resource + operation combination */
type ResourceScope<
	R extends Resource,
	Operation extends (typeof RESOURCES)[R][number] = (typeof RESOURCES)[R][number],
> = `${R}:${Operation}`;

/** A wildcard scope applies to all operations on a resource or all resources */
type WildcardScope = `${Resource}:*` | '*';

// This is purely an intermediary type.
// If we tried to do use `ResourceScope<Resource>` directly we'd end
// up with all resources having all scopes (e.g. `ldap:uninstall`).
type AllScopesObject = {
	[R in Resource]: ResourceScope<R>;
};

/** A permission scope in the system, either a specific resource:operation or a wildcard */
export type Scope = AllScopesObject[Resource] | WildcardScope;

export type ScopeLevels = {
	global: Scope[];
	project?: Scope[];
	resource?: Scope[];
};

export type MaskLevels = {
	sharing: Scope[];
};

export type ScopeOptions = { mode: 'oneOf' | 'allOf' };

export type RoleNamespace = z.infer<typeof roleNamespaceSchema>;
export type GlobalRole = z.infer<typeof globalRoleSchema>;
export type AssignableGlobalRole = z.infer<typeof assignableGlobalRoleSchema>;
export type CredentialSharingRole = z.infer<typeof credentialSharingRoleSchema>;
export type WorkflowSharingRole = z.infer<typeof workflowSharingRoleSchema>;
export type TeamProjectRole = z.infer<typeof teamRoleSchema>;
export type ProjectRole = z.infer<typeof systemProjectRoleSchema>;
export type AssignableProjectRole = z.infer<typeof assignableProjectRoleSchema>;

/**
 * Type guard for assignable project role slugs.
 *
 * Custom project roles are supported. We consider any slug that:
 * - starts with the `project:` prefix, and
 * - is not the personal owner role
 * to be an assignable project role.
 */
export function isAssignableProjectRoleSlug(slug: string): slug is AssignableProjectRole {
	return slug.startsWith('project:') && slug !== PROJECT_OWNER_ROLE_SLUG;
}

/** Union of all possible role types in the system */
export type AllRoleTypes = GlobalRole | ProjectRole | WorkflowSharingRole | CredentialSharingRole;

export type AllRolesMap = {
	global: Role[];
	project: Role[];
	credential: Role[];
	workflow: Role[];
};

export type DbScope = {
	slug: Scope;
};

export type DbRole = {
	slug: string;
	scopes: DbScope[];
};

/**
 * Represents an authenticated entity in the system that can have specific permissions via a role.
 * @property role - The global role this principal has
 */
export type AuthPrincipal = {
	role: DbRole;
};

// #region Public API
type PublicApiKeyResources = keyof typeof API_KEY_RESOURCES;

type ApiKeyResourceScope<
	R extends PublicApiKeyResources,
	Operation extends (typeof API_KEY_RESOURCES)[R][number] = (typeof API_KEY_RESOURCES)[R][number],
> = `${R}:${Operation}`;

// This is purely an intermediary type.
// If we tried to do use `ResourceScope<Resource>` directly we'd end
// up with all resources having all scopes.
type AllApiKeyScopesObject = {
	[R in PublicApiKeyResources]: ApiKeyResourceScope<R>;
};

export type ApiKeyScope = AllApiKeyScopesObject[PublicApiKeyResources];

export function isApiKeyScope(scope: Scope): scope is ApiKeyScope {
	// We are casting with as for runtime type checking
	return ALL_API_KEY_SCOPES.has(scope as ApiKeyScope);
}

// #endregion
