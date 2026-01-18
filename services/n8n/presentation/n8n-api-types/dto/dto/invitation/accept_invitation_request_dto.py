"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/invitation/accept-invitation-request.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/invitation 的模块。导入/依赖:外部:zod、zod-class；内部:无；本地:../schemas/password.schema。导出:AcceptInvitationRequestDto。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/invitation/accept-invitation-request.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/invitation/accept_invitation_request_dto.py

import { z } from 'zod';
import { Z } from 'zod-class';

import { passwordSchema } from '../../schemas/password.schema';

// Support both legacy format (inviterId) and new JWT format (token)
// All fields are optional at the schema level, but validation ensures either token OR inviterId is provided
export class AcceptInvitationRequestDto extends Z.class({
	inviterId: z.string().uuid().optional(),
	inviteeId: z.string().uuid().optional(),
	token: z.string().optional(),
	firstName: z.string().min(1, 'First name is required'),
	lastName: z.string().min(1, 'Last name is required'),
	password: passwordSchema,
}) {}
