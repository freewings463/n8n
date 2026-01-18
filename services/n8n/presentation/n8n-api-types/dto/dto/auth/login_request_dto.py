"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/auth/login-request.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/auth 的认证模块。导入/依赖:外部:zod、zod-class；内部:无；本地:无。导出:LoginRequestDto。关键函数/方法:无。用于承载认证实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/auth/login-request.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/auth/login_request_dto.py

import { z } from 'zod';
import { Z } from 'zod-class';

export class LoginRequestDto extends Z.class({
	/*
	 * The LDAP username does not need to be an email, so email validation
	 * is not enforced here. The controller determines whether this is an
	 * email and validates when LDAP is disabled
	 */
	emailOrLdapLoginId: z.string().trim(),
	password: z.string().min(1),
	mfaCode: z.string().optional(),
	mfaRecoveryCode: z.string().optional(),
}) {}
