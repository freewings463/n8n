"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/roles/create-role.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/roles 的模块。导入/依赖:外部:zod、zod-class；内部:@n8n/permissions；本地:无。导出:CreateRoleDto。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/roles/create-role.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/roles/create_role_dto.py

import { scopeSchema } from '@n8n/permissions';
import { z } from 'zod';
import { Z } from 'zod-class';

export class CreateRoleDto extends Z.class({
	displayName: z.string().min(2).max(100),
	description: z.string().max(500).optional(),
	roleType: z.enum(['project']),
	scopes: z.array(scopeSchema),
}) {}
