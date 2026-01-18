"""
MIGRATION-META:
  source_path: packages/cli/src/auth/jwt.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/auth 的认证模块。导入/依赖:外部:express；内部:@n8n/db、@n8n/di；本地:./auth.service。导出:issueCookie。关键函数/方法:issueCookie。用于承载认证实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/auth/jwt.ts -> services/n8n/presentation/cli/api/auth/jwt.py

import type { User } from '@n8n/db';
import { Container } from '@n8n/di';
import type { Response } from 'express';

import { AuthService } from './auth.service';

// This method is still used by cloud hooks.
// DO NOT DELETE until the hooks have been updated
/** @deprecated Use `AuthService` instead */
export function issueCookie(res: Response, user: User) {
	return Container.get(AuthService).issueCookie(res, user, user.mfaEnabled);
}
