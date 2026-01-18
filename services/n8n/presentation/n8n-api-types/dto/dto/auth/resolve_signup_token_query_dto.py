"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/auth/resolve-signup-token-query.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/auth 的认证模块。导入/依赖:外部:zod、zod-class；内部:无；本地:无。导出:ResolveSignupTokenQueryDto。关键函数/方法:无。用于承载认证实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/auth/resolve-signup-token-query.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/auth/resolve_signup_token_query_dto.py

import { z } from 'zod';
import { Z } from 'zod-class';

// Support both legacy format (inviterId + inviteeId) and new JWT format (token)
// All fields are optional at the schema level, but validation ensures either token OR (inviterId AND inviteeId) are provided
const resolveSignupTokenShape = {
	inviterId: z.string().uuid().optional(),
	inviteeId: z.string().uuid().optional(),
	token: z.string().optional(),
};

export class ResolveSignupTokenQueryDto extends Z.class(resolveSignupTokenShape) {}
