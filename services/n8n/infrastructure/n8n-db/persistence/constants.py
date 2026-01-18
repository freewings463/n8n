"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src 的模块。导入/依赖:外部:entities；内部:无；本地:无。导出:builtInRoleToRoleObject、ALL_BUILTIN_ROLES、GLOBAL_OWNER_ROLE、GLOBAL_ADMIN_ROLE、GLOBAL_MEMBER_ROLE、GLOBAL_CHAT_USER_ROLE、PROJECT_OWNER_ROLE、PROJECT_ADMIN_ROLE 等5项。关键函数/方法:builtInRoleToRoleObject、toRoleMap。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package @n8n/db defaulted to persistence infrastructure
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/constants.ts -> services/n8n/infrastructure/n8n-db/persistence/constants.py

import {
	PROJECT_ADMIN_ROLE_SLUG,
	PROJECT_EDITOR_ROLE_SLUG,
	PROJECT_OWNER_ROLE_SLUG,
	PROJECT_VIEWER_ROLE_SLUG,
	PROJECT_CHAT_USER_ROLE_SLUG,
	ALL_ROLES,
	type ProjectRole,
	type GlobalRole,
	type Role as RoleDTO,
} from '@n8n/permissions';

import type { Role } from 'entities';

export function builtInRoleToRoleObject(
	role: RoleDTO,
	roleType: 'global' | 'project' | 'workflow' | 'credential',
): Role {
	return {
		slug: role.slug,
		displayName: role.displayName,
		scopes: role.scopes.map((scope) => {
			return {
				slug: scope,
				displayName: scope,
				description: null,
			};
		}),
		systemRole: true,
		roleType,
		description: role.description,
	} as Role;
}

function toRoleMap(allRoles: Role[]): Record<string, Role> {
	return allRoles.reduce(
		(acc, role) => {
			acc[role.slug] = role;
			return acc;
		},
		{} as Record<string, Role>,
	);
}

export const ALL_BUILTIN_ROLES = toRoleMap([
	...ALL_ROLES.global.map((role) => builtInRoleToRoleObject(role, 'global')),
	...ALL_ROLES.project.map((role) => builtInRoleToRoleObject(role, 'project')),
	...ALL_ROLES.credential.map((role) => builtInRoleToRoleObject(role, 'credential')),
	...ALL_ROLES.workflow.map((role) => builtInRoleToRoleObject(role, 'workflow')),
]);

export const GLOBAL_OWNER_ROLE = ALL_BUILTIN_ROLES['global:owner'];
export const GLOBAL_ADMIN_ROLE = ALL_BUILTIN_ROLES['global:admin'];
export const GLOBAL_MEMBER_ROLE = ALL_BUILTIN_ROLES['global:member'];
export const GLOBAL_CHAT_USER_ROLE = ALL_BUILTIN_ROLES['global:chatUser'];

export const PROJECT_OWNER_ROLE = ALL_BUILTIN_ROLES[PROJECT_OWNER_ROLE_SLUG];
export const PROJECT_ADMIN_ROLE = ALL_BUILTIN_ROLES[PROJECT_ADMIN_ROLE_SLUG];
export const PROJECT_EDITOR_ROLE = ALL_BUILTIN_ROLES[PROJECT_EDITOR_ROLE_SLUG];
export const PROJECT_VIEWER_ROLE = ALL_BUILTIN_ROLES[PROJECT_VIEWER_ROLE_SLUG];
export const PROJECT_CHAT_USER_ROLE = ALL_BUILTIN_ROLES[PROJECT_CHAT_USER_ROLE_SLUG];

export const GLOBAL_ROLES: Record<GlobalRole, Role> = {
	'global:owner': GLOBAL_OWNER_ROLE,
	'global:admin': GLOBAL_ADMIN_ROLE,
	'global:member': GLOBAL_MEMBER_ROLE,
	'global:chatUser': GLOBAL_CHAT_USER_ROLE,
};

export const PROJECT_ROLES: Record<ProjectRole, Role> = {
	[PROJECT_OWNER_ROLE_SLUG]: PROJECT_OWNER_ROLE,
	[PROJECT_ADMIN_ROLE_SLUG]: PROJECT_ADMIN_ROLE,
	[PROJECT_EDITOR_ROLE_SLUG]: PROJECT_EDITOR_ROLE,
	[PROJECT_VIEWER_ROLE_SLUG]: PROJECT_VIEWER_ROLE,
	[PROJECT_CHAT_USER_ROLE_SLUG]: PROJECT_CHAT_USER_ROLE,
};
