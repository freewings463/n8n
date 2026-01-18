"""
MIGRATION-META:
  source_path: packages/cli/src/ldap.ee/types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/ldap.ee 的LDAP类型。导入/依赖:外部:无；内部:@n8n/constants、@n8n/db；本地:无。导出:无。关键函数/方法:无。用于定义LDAP相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/ldap.ee/types.ts -> services/n8n/application/cli/services/ldap.ee/types.py

import type { LdapConfig } from '@n8n/constants';
import type { AuthenticatedRequest, RunningMode } from '@n8n/db';

export declare namespace LdapConfiguration {
	type Update = AuthenticatedRequest<{}, {}, LdapConfig, {}>;
	type Sync = AuthenticatedRequest<{}, {}, { type: RunningMode }, {}>;
	type GetSync = AuthenticatedRequest<{}, {}, {}, { page?: string; perPage?: string }>;
}
