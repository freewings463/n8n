"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/utils/is-valid-email.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/utils 的工具。导入/依赖:外部:zod；内部:无；本地:无。导出:isValidEmail。关键函数/方法:isValidEmail。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package @n8n/db defaulted to persistence infrastructure
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/utils/is-valid-email.ts -> services/n8n/infrastructure/n8n-db/persistence/utils/is_valid_email.py

import { z } from 'zod';

export function isValidEmail(email: string): boolean {
	return z.string().email().safeParse(email).success;
}
