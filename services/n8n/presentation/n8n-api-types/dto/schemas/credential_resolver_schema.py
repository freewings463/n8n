"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/schemas/credential-resolver.schema.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/schemas 的模块。导入/依赖:外部:zod；内部:无；本地:无。导出:credentialResolverIdSchema、credentialResolverNameSchema、credentialResolverTypeNameSchema、credentialResolverConfigSchema、credentialResolverSchema、credentialResolverTypeSchema、credentialResolverTypesSchema、CredentialResolverType 等2项。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/schemas/credential-resolver.schema.ts -> services/n8n/presentation/n8n-api-types/dto/schemas/credential_resolver_schema.py

import { z } from 'zod';

export const credentialResolverIdSchema = z.string().max(36);
export const credentialResolverNameSchema = z.string().trim().min(1).max(255);
export const credentialResolverTypeNameSchema = z.string().trim().min(1).max(255);
export const credentialResolverConfigSchema = z.record(z.unknown());

export const credentialResolverSchema = z.object({
	id: credentialResolverIdSchema,
	name: credentialResolverNameSchema,
	type: credentialResolverTypeNameSchema,
	config: z.string(), // Encrypted config
	decryptedConfig: credentialResolverConfigSchema.optional(),
	createdAt: z.coerce.date(),
	updatedAt: z.coerce.date(),
});

export const credentialResolverTypeSchema = z.object({
	name: credentialResolverTypeNameSchema,
	displayName: z.string().trim().min(1).max(255),
	description: z.string().trim().max(1024).optional(),
	options: z.array(z.record(z.unknown())).optional(),
});

export const credentialResolverTypesSchema = z.array(credentialResolverTypeSchema);

export type CredentialResolverType = z.infer<typeof credentialResolverTypeSchema>;

export const credentialResolversSchema = z.array(credentialResolverSchema);

export type CredentialResolver = z.infer<typeof credentialResolverSchema>;
