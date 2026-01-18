"""
MIGRATION-META:
  source_path: packages/cli/src/controllers/oauth/oauth2-dynamic-client-registration.schema.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/controllers/oauth 的OAuth控制器。导入/依赖:外部:zod/v4；内部:无；本地:无。导出:oAuthAuthorizationServerMetadataSchema、dynamicClientRegistrationResponseSchema。关键函数/方法:无。用于处理OAuth接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Controller -> presentation/api/v1/controllers
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/controllers/oauth/oauth2-dynamic-client-registration.schema.ts -> services/n8n/presentation/cli/api/v1/controllers/oauth/oauth2_dynamic_client_registration_schema.py

import { z } from 'zod/v4';

export const oAuthAuthorizationServerMetadataSchema = z.object({
	authorization_endpoint: z.url({ protocol: /^https?$/ }),
	token_endpoint: z.url({ protocol: /^https?$/ }),
	registration_endpoint: z.url({ protocol: /^https?$/ }),
	grant_types_supported: z.array(z.string()).optional(),
	token_endpoint_auth_methods_supported: z.array(z.string()).optional(),
	code_challenge_methods_supported: z.array(z.string()).optional(),
	scopes_supported: z.array(z.string()).optional(),
});

export const dynamicClientRegistrationResponseSchema = z.object({
	client_id: z.string(),
	client_secret: z.string().optional(),
});
