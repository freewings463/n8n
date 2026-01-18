"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/saml/saml-preferences.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/saml 的模块。导入/依赖:外部:zod、zod-class；内部:无；本地:无。导出:SamlPreferencesAttributeMapping、SamlPreferences。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/saml/saml-preferences.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/saml/saml_preferences_dto.py

import { z } from 'zod';
import { Z } from 'zod-class';

const SamlLoginBindingSchema = z.enum(['redirect', 'post']);

/** Schema for configuring the signature in SAML requests/responses. */
const SignatureConfigSchema = z.object({
	prefix: z.string().default('ds'),
	location: z.object({
		reference: z.string(),
		action: z.enum(['before', 'after', 'prepend', 'append']),
	}),
});

export class SamlPreferencesAttributeMapping extends Z.class({
	/** SAML attribute mapped to the user's email. */
	email: z.string(),
	/** SAML attribute mapped to the user's first name. */
	firstName: z.string(),
	/** SAML attribute mapped to the user's last name. */
	lastName: z.string(),
	/** SAML attribute mapped to the user's principal name. */
	userPrincipalName: z.string(),
	/** SAML attribute mapped to the n8n instance role. */
	n8nInstanceRole: z.string().optional(),
	/** Each element in the array is formatted like "<projectId>:<role>" */
	n8nProjectRoles: z.array(z.string()).optional(),
}) {}

export class SamlPreferences extends Z.class({
	/** Mapping of SAML attributes to user fields. */
	mapping: SamlPreferencesAttributeMapping.optional(),
	/** SAML metadata in XML format. */
	metadata: z.string().optional(),
	metadataUrl: z.string().optional(),

	ignoreSSL: z.boolean().default(false),
	loginBinding: SamlLoginBindingSchema.default('redirect'),
	/** Whether SAML login is enabled. */
	loginEnabled: z.boolean().optional(),
	/** Label for the SAML login button. on the Auth screen */
	loginLabel: z.string().optional(),

	authnRequestsSigned: z.boolean().default(false),
	wantAssertionsSigned: z.boolean().default(true),
	wantMessageSigned: z.boolean().default(true),

	acsBinding: SamlLoginBindingSchema.default('post'),
	signatureConfig: SignatureConfigSchema.default({
		prefix: 'ds',
		location: {
			reference: '/samlp:Response/saml:Issuer',
			action: 'after',
		},
	}),

	relayState: z.string().default(''),
}) {}
