"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/user/role-change-request.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/user 的模块。导入/依赖:外部:zod-class；内部:@n8n/permissions；本地:无。导出:RoleChangeRequestDto。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/user/role-change-request.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/user/role_change_request_dto.py

import { assignableGlobalRoleSchema } from '@n8n/permissions';
import { Z } from 'zod-class';

export class RoleChangeRequestDto extends Z.class({
	newRoleName: assignableGlobalRoleSchema
		// enforce required (non-nullable, non-optional) with custom error message on undefined
		.nullish()
		.refine((val): val is NonNullable<typeof val> => val !== null && typeof val !== 'undefined', {
			message: 'New role is required',
		}),
}) {}
