"""
MIGRATION-META:
  source_path: packages/cli/src/modules/dynamic-credentials.ee/context-establishment-hooks/bearer-token-extractor.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/dynamic-credentials.ee/context-establishment-hooks 的模块。导入/依赖:外部:无；内部:无；本地:./http-header-extractor。导出:BearerTokenExtractor。关键函数/方法:execute、isApplicableToTriggerNode。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/dynamic-credentials.ee/context-establishment-hooks/bearer-token-extractor.ts -> services/n8n/application/cli/services/modules/dynamic-credentials.ee/context-establishment-hooks/bearer_token_extractor.py

import {
	ContextEstablishmentHook,
	ContextEstablishmentOptions,
	ContextEstablishmentResult,
	HookDescription,
	IContextEstablishmentHook,
} from '@n8n/decorators';

import { HttpHeaderExtractor } from './http-header-extractor';

/**
 * Extracts bearer tokens from the Authorization HTTP header.
 *
 * Automatically extracts tokens from headers in the format:
 * - `Authorization: Bearer <token>`
 * - Case-insensitive "Bearer" prefix
 *
 * The extracted token becomes the credential identity for OAuth2 introspection.
 *
 * @example
 * // Request header:
 * // Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
 *
 * // Result:
 * // context.credentials.identity = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
 */
@ContextEstablishmentHook()
export class BearerTokenExtractor implements IContextEstablishmentHook {
	constructor(private readonly httpHeaderExtractor: HttpHeaderExtractor) {}

	hookDescription: HookDescription = {
		name: 'BearerTokenExtractor',
		displayName: 'Bearer Token Extractor',
		options: [],
	};

	isApplicableToTriggerNode(nodeType: string): boolean {
		return this.httpHeaderExtractor.isApplicableToTriggerNode(nodeType);
	}

	async execute(options: ContextEstablishmentOptions): Promise<ContextEstablishmentResult> {
		return await this.httpHeaderExtractor.execute({
			...options,
			options: {
				headerName: 'authorization',
				headerValue: '[Bb][Ee][Aa][Rr][Ee][Rr]\\s+(.+)',
			},
		});
	}
}
