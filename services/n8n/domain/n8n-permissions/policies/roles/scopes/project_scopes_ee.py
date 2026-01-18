"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/src/roles/scopes/project-scopes.ee.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions/src/roles/scopes 的模块。导入/依赖:外部:无；内部:无；本地:../../types.ee。导出:REGULAR_PROJECT_ADMIN_SCOPES、PERSONAL_PROJECT_OWNER_SCOPES、PROJECT_EDITOR_SCOPES、PROJECT_VIEWER_SCOPES、PROJECT_CHAT_USER_SCOPES。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/src/roles/scopes/project-scopes.ee.ts -> services/n8n/domain/n8n-permissions/policies/roles/scopes/project_scopes_ee.py

import type { Scope } from '../../types.ee';

/**
 * Diff between admin in personal project and admin in other projects:
 * - You cannot rename your personal project.
 * - You cannot invite people to your personal project.
 */

export const REGULAR_PROJECT_ADMIN_SCOPES: Scope[] = [
	'workflow:create',
	'workflow:read',
	'workflow:update',
	'workflow:publish',
	'workflow:delete',
	'workflow:list',
	'workflow:execute',
	'workflow:execute-chat',
	'workflow:move',
	'credential:create',
	'credential:read',
	'credential:update',
	'credential:delete',
	'credential:list',
	'credential:move',
	'credential:share',
	'project:list',
	'project:read',
	'project:update',
	'project:delete',
	'folder:create',
	'folder:read',
	'folder:update',
	'folder:delete',
	'folder:list',
	'folder:move',
	'sourceControl:push',
	'dataTable:create',
	'dataTable:delete',
	'dataTable:read',
	'dataTable:update',
	'dataTable:listProject',
	'dataTable:readRow',
	'dataTable:writeRow',
	'projectVariable:list',
	'projectVariable:read',
	'projectVariable:create',
	'projectVariable:update',
	'projectVariable:delete',
];

export const PERSONAL_PROJECT_OWNER_SCOPES: Scope[] = [
	'workflow:create',
	'workflow:read',
	'workflow:update',
	'workflow:publish',
	'workflow:delete',
	'workflow:list',
	'workflow:execute',
	'workflow:execute-chat',
	'workflow:share',
	'workflow:move',
	'credential:create',
	'credential:read',
	'credential:update',
	'credential:delete',
	'credential:list',
	'credential:share',
	'credential:move',
	'project:list',
	'project:read',
	'folder:create',
	'folder:read',
	'folder:update',
	'folder:delete',
	'folder:list',
	'folder:move',
	'dataTable:create',
	'dataTable:delete',
	'dataTable:read',
	'dataTable:update',
	'dataTable:listProject',
	'dataTable:readRow',
	'dataTable:writeRow',
];

export const PROJECT_EDITOR_SCOPES: Scope[] = [
	'workflow:create',
	'workflow:read',
	'workflow:update',
	'workflow:publish',
	'workflow:delete',
	'workflow:list',
	'workflow:execute',
	'workflow:execute-chat',
	'credential:create',
	'credential:read',
	'credential:update',
	'credential:delete',
	'credential:list',
	'project:list',
	'project:read',
	'folder:create',
	'folder:read',
	'folder:update',
	'folder:delete',
	'folder:list',
	'dataTable:create',
	'dataTable:delete',
	'dataTable:read',
	'dataTable:update',
	'dataTable:listProject',
	'dataTable:readRow',
	'dataTable:writeRow',
	'projectVariable:list',
	'projectVariable:read',
	'projectVariable:create',
	'projectVariable:update',
	'projectVariable:delete',
];

export const PROJECT_VIEWER_SCOPES: Scope[] = [
	'credential:list',
	'credential:read',
	'project:list',
	'project:read',
	'workflow:list',
	'workflow:read',
	'workflow:execute-chat',
	'folder:read',
	'folder:list',
	'dataTable:listProject',
	'dataTable:read',
	'dataTable:readRow',
	'projectVariable:list',
	'projectVariable:read',
];

export const PROJECT_CHAT_USER_SCOPES: Scope[] = ['workflow:execute-chat'];
