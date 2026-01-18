"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/oidc/config.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/oidc 的配置。导入/依赖:外部:zod、zod-class；内部:无；本地:无。导出:OidcConfigDto。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/oidc/config.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/oidc/config_dto.py

import { z } from 'zod';
import { Z } from 'zod-class';

export class OidcConfigDto extends Z.class({
	clientId: z.string().min(1),
	clientSecret: z.string().min(1),
	discoveryEndpoint: z.string().url(),
	loginEnabled: z.boolean().optional().default(false),
	prompt: z
		.enum(['none', 'login', 'consent', 'select_account', 'create'])
		.optional()
		.default('select_account'),
	authenticationContextClassReference: z.array(z.string()).default([]),
}) {}
