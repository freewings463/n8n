"""
MIGRATION-META:
  source_path: packages/@n8n/permissions/src/roles/scopes/credential-sharing-scopes.ee.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/permissions/src/roles/scopes 的模块。导入/依赖:外部:无；内部:无；本地:../../types.ee。导出:CREDENTIALS_SHARING_OWNER_SCOPES、CREDENTIALS_SHARING_USER_SCOPES。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/permissions treated as domain authorization policies
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/permissions/src/roles/scopes/credential-sharing-scopes.ee.ts -> services/n8n/domain/n8n-permissions/policies/roles/scopes/credential_sharing_scopes_ee.py

import type { Scope } from '../../types.ee';

export const CREDENTIALS_SHARING_OWNER_SCOPES: Scope[] = [
	'credential:read',
	'credential:update',
	'credential:delete',
	'credential:share',
	'credential:move',
];

export const CREDENTIALS_SHARING_USER_SCOPES: Scope[] = ['credential:read'];
