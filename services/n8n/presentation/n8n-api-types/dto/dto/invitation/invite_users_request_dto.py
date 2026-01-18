"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/invitation/invite-users-request.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/invitation 的模块。导入/依赖:外部:zod；内部:@n8n/permissions；本地:无。导出:InviteUsersRequestDto。关键函数/方法:safeParse。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/invitation/invite-users-request.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/invitation/invite_users_request_dto.py

import { assignableGlobalRoleSchema } from '@n8n/permissions';
import { z } from 'zod';

const invitedUserSchema = z.object({
	email: z.string().email(),
	role: assignableGlobalRoleSchema.default('global:member'),
});

const invitationsSchema = z.array(invitedUserSchema);

export class InviteUsersRequestDto extends Array<z.infer<typeof invitedUserSchema>> {
	static safeParse(data: unknown) {
		return invitationsSchema.safeParse(data);
	}
}
