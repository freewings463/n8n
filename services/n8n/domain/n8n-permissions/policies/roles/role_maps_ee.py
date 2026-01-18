"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/src/roles/role-maps.ee.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions/src/roles 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:GLOBAL_SCOPE_MAP、PROJECT_SCOPE_MAP、CREDENTIALS_SHARING_SCOPE_MAP、WORKFLOW_SHARING_SCOPE_MAP、ALL_ROLE_MAPS。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。注释目标:eslint-disable @typescript-eslint/naming-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/src/roles/role-maps.ee.ts -> services/n8n/domain/n8n-permissions/policies/roles/role_maps_ee.py

/* eslint-disable @typescript-eslint/naming-convention */
import type {
	CredentialSharingRole,
	GlobalRole,
	ProjectRole,
	Scope,
	WorkflowSharingRole,
} from '../types.ee';
import {
	CREDENTIALS_SHARING_OWNER_SCOPES,
	CREDENTIALS_SHARING_USER_SCOPES,
} from './scopes/credential-sharing-scopes.ee';
import {
	GLOBAL_OWNER_SCOPES,
	GLOBAL_ADMIN_SCOPES,
	GLOBAL_MEMBER_SCOPES,
	GLOBAL_CHAT_USER_SCOPES,
} from './scopes/global-scopes.ee';
import {
	REGULAR_PROJECT_ADMIN_SCOPES,
	PERSONAL_PROJECT_OWNER_SCOPES,
	PROJECT_EDITOR_SCOPES,
	PROJECT_VIEWER_SCOPES,
	PROJECT_CHAT_USER_SCOPES,
} from './scopes/project-scopes.ee';
import {
	WORKFLOW_SHARING_OWNER_SCOPES,
	WORKFLOW_SHARING_EDITOR_SCOPES,
} from './scopes/workflow-sharing-scopes.ee';

export const GLOBAL_SCOPE_MAP: Record<GlobalRole, Scope[]> = {
	'global:owner': GLOBAL_OWNER_SCOPES,
	'global:admin': GLOBAL_ADMIN_SCOPES,
	'global:member': GLOBAL_MEMBER_SCOPES,
	'global:chatUser': GLOBAL_CHAT_USER_SCOPES,
};

export const PROJECT_SCOPE_MAP: Record<ProjectRole, Scope[]> = {
	'project:admin': REGULAR_PROJECT_ADMIN_SCOPES,
	'project:personalOwner': PERSONAL_PROJECT_OWNER_SCOPES,
	'project:editor': PROJECT_EDITOR_SCOPES,
	'project:viewer': PROJECT_VIEWER_SCOPES,
	'project:chatUser': PROJECT_CHAT_USER_SCOPES,
};

export const CREDENTIALS_SHARING_SCOPE_MAP: Record<CredentialSharingRole, Scope[]> = {
	'credential:owner': CREDENTIALS_SHARING_OWNER_SCOPES,
	'credential:user': CREDENTIALS_SHARING_USER_SCOPES,
};

export const WORKFLOW_SHARING_SCOPE_MAP: Record<WorkflowSharingRole, Scope[]> = {
	'workflow:owner': WORKFLOW_SHARING_OWNER_SCOPES,
	'workflow:editor': WORKFLOW_SHARING_EDITOR_SCOPES,
};

export const ALL_ROLE_MAPS = {
	global: GLOBAL_SCOPE_MAP,
	project: PROJECT_SCOPE_MAP,
	credential: CREDENTIALS_SHARING_SCOPE_MAP,
	workflow: WORKFLOW_SHARING_SCOPE_MAP,
} as const;
