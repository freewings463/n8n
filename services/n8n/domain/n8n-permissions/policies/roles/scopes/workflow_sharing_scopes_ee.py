"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/src/roles/scopes/workflow-sharing-scopes.ee.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions/src/roles/scopes 的工作流模块。导入/依赖:外部:无；内部:无；本地:../../types.ee。导出:WORKFLOW_SHARING_OWNER_SCOPES、WORKFLOW_SHARING_EDITOR_SCOPES。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/src/roles/scopes/workflow-sharing-scopes.ee.ts -> services/n8n/domain/n8n-permissions/policies/roles/scopes/workflow_sharing_scopes_ee.py

import type { Scope } from '../../types.ee';

export const WORKFLOW_SHARING_OWNER_SCOPES: Scope[] = [
	'workflow:read',
	'workflow:update',
	'workflow:publish',
	'workflow:delete',
	'workflow:execute',
	'workflow:share',
	'workflow:move',
	'workflow:execute-chat',
];

export const WORKFLOW_SHARING_EDITOR_SCOPES: Scope[] = [
	'workflow:read',
	'workflow:update',
	'workflow:publish',
	'workflow:execute',
	'workflow:execute-chat',
];
