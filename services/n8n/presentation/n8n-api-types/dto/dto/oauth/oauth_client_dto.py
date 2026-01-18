"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/oauth/oauth-client.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/oauth 的OAuth模块。导入/依赖:外部:zod、zod-class；内部:无；本地:无。导出:OAuthClientResponseDto、ListOAuthClientsResponseDto、DeleteOAuthClientResponseDto。关键函数/方法:无。用于承载OAuth实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/oauth/oauth-client.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/oauth/oauth_client_dto.py

import { z } from 'zod';
import { Z } from 'zod-class';

/**
 * DTO for OAuth client response (excludes sensitive data like clientSecret)
 */
export class OAuthClientResponseDto extends Z.class({
	id: z.string(),
	name: z.string(),
	redirectUris: z.array(z.string()),
	grantTypes: z.array(z.string()),
	tokenEndpointAuthMethod: z.string(),
	createdAt: z.string().datetime(), // Using string for date serialization over HTTP
	updatedAt: z.string().datetime(),
}) {}

/**
 * DTO for listing OAuth clients response
 */
export class ListOAuthClientsResponseDto extends Z.class({
	data: z.array(
		z.object({
			id: z.string(),
			name: z.string(),
			redirectUris: z.array(z.string()),
			grantTypes: z.array(z.string()),
			tokenEndpointAuthMethod: z.string(),
			createdAt: z.string().datetime(),
			updatedAt: z.string().datetime(),
		}),
	),
	count: z.number(),
}) {}

/**
 * DTO for deleting an OAuth client response
 */
export class DeleteOAuthClientResponseDto extends Z.class({
	success: z.boolean(),
	message: z.string(),
}) {}
