"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/api-keys.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src 的模块。导入/依赖:外部:无；内部:@n8n/permissions；本地:无。导出:UnixTimestamp、ApiKey、ApiKeyWithRawValue、ApiKeyAudience。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/api-keys.ts -> services/n8n/presentation/n8n-api-types/dto/api_keys.py

import type { ApiKeyScope } from '@n8n/permissions';

/** Unix timestamp. Seconds since epoch */
export type UnixTimestamp = number | null;

export type ApiKey = {
	id: string;
	label: string;
	apiKey: string;
	createdAt: string;
	updatedAt: string;
	/** Null if API key never expires */
	expiresAt: UnixTimestamp | null;
	scopes: ApiKeyScope[];
};

export type ApiKeyWithRawValue = ApiKey & { rawApiKey: string };

export type ApiKeyAudience = 'public-api' | 'mcp-server-api';
