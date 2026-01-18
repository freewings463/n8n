"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/src/roles/all-roles.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions/src/roles 的模块。导入/依赖:外部:无；内部:无；本地:../types.ee、../utilities/get-role-scopes.ee。导出:ALL_ROLES、isBuiltInRole。关键函数/方法:isBuiltInRole。用于承载该模块实现细节，并通过导出对外提供能力。注释目标:eslint-disable @typescript-eslint/naming-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/src/roles/all-roles.ts -> services/n8n/domain/n8n-permissions/policies/roles/all_roles.py

/* eslint-disable @typescript-eslint/naming-convention */
import {
	PROJECT_ADMIN_ROLE_SLUG,
	PROJECT_EDITOR_ROLE_SLUG,
	PROJECT_OWNER_ROLE_SLUG,
	PROJECT_VIEWER_ROLE_SLUG,
	PROJECT_CHAT_USER_ROLE_SLUG,
} from '../constants.ee';
import {
	CREDENTIALS_SHARING_SCOPE_MAP,
	GLOBAL_SCOPE_MAP,
	PROJECT_SCOPE_MAP,
	WORKFLOW_SHARING_SCOPE_MAP,
} from './role-maps.ee';
import type { AllRolesMap, AllRoleTypes, Scope } from '../types.ee';
import { getRoleScopes } from '../utilities/get-role-scopes.ee';

const ROLE_NAMES: Record<AllRoleTypes, string> = {
	'global:owner': 'Owner',
	'global:admin': 'Admin',
	'global:member': 'Member',
	'global:chatUser': 'Chat User',
	[PROJECT_OWNER_ROLE_SLUG]: 'Project Owner',
	[PROJECT_ADMIN_ROLE_SLUG]: 'Project Admin',
	[PROJECT_EDITOR_ROLE_SLUG]: 'Project Editor',
	[PROJECT_VIEWER_ROLE_SLUG]: 'Project Viewer',
	[PROJECT_CHAT_USER_ROLE_SLUG]: 'Project Chat User',
	'credential:user': 'Credential User',
	'credential:owner': 'Credential Owner',
	'workflow:owner': 'Workflow Owner',
	'workflow:editor': 'Workflow Editor',
};

const ROLE_DESCRIPTIONS: Record<AllRoleTypes, string> = {
	'global:owner': 'Owner',
	'global:admin': 'Admin',
	'global:member': 'Member',
	'global:chatUser': 'Chat User',
	[PROJECT_OWNER_ROLE_SLUG]: 'Project Owner',
	[PROJECT_ADMIN_ROLE_SLUG]:
		'Full control of settings, members, workflows, credentials and executions',
	[PROJECT_EDITOR_ROLE_SLUG]: 'Create, edit, and delete workflows, credentials, and executions',
	[PROJECT_VIEWER_ROLE_SLUG]: 'Read-only access to workflows, credentials, and executions',
	[PROJECT_CHAT_USER_ROLE_SLUG]:
		'Chat-only access to chatting with workflows that have n8n Chat enabled',
	'credential:user': 'Credential User',
	'credential:owner': 'Credential Owner',
	'workflow:owner': 'Workflow Owner',
	'workflow:editor': 'Workflow Editor',
};

const mapToRoleObject = <T extends keyof typeof ROLE_NAMES>(
	roles: Record<T, Scope[]>,
	roleType: 'global' | 'project' | 'credential' | 'workflow',
) =>
	(Object.keys(roles) as T[]).map((role) => ({
		slug: role,
		displayName: ROLE_NAMES[role],
		scopes: getRoleScopes(role),
		description: ROLE_DESCRIPTIONS[role],
		licensed: false,
		systemRole: true,
		roleType,
	}));

export const ALL_ROLES: AllRolesMap = {
	global: mapToRoleObject(GLOBAL_SCOPE_MAP, 'global'),
	project: mapToRoleObject(PROJECT_SCOPE_MAP, 'project'),
	credential: mapToRoleObject(CREDENTIALS_SHARING_SCOPE_MAP, 'credential'),
	workflow: mapToRoleObject(WORKFLOW_SHARING_SCOPE_MAP, 'workflow'),
};

export const isBuiltInRole = (role: string): role is AllRoleTypes => {
	return Object.prototype.hasOwnProperty.call(ROLE_NAMES, role);
};
