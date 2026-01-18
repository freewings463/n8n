"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/credentials/create-credential.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/credentials 的凭证。导入/依赖:外部:zod、zod-class；内部:无；本地:无。导出:CreateCredentialDto。关键函数/方法:无。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/credentials/create-credential.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/credentials/create_credential_dto.py

import { z } from 'zod';
import { Z } from 'zod-class';

export class CreateCredentialDto extends Z.class({
	name: z.string().min(1).max(128),
	type: z.string().min(1).max(128),
	data: z.record(z.string(), z.unknown()),
	projectId: z.string().optional(),
	uiContext: z.string().optional(),
	isGlobal: z.boolean().optional(),
	isResolvable: z.boolean().optional(),
}) {}
