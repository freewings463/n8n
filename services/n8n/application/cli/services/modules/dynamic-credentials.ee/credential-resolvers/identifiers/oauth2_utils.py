"""
MIGRATION-META:
  source_path: packages/cli/src/modules/dynamic-credentials.ee/credential-resolvers/identifiers/oauth2-utils.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/dynamic-credentials.ee/credential-resolvers 的OAuth模块。导入/依赖:外部:zod；内部:无；本地:无。导出:OAuth2OptionsSchema、OAuth2Options、sha256。关键函数/方法:sha256。用于承载OAuth实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/dynamic-credentials.ee/credential-resolvers/identifiers/oauth2-utils.ts -> services/n8n/application/cli/services/modules/dynamic-credentials.ee/credential-resolvers/identifiers/oauth2_utils.py

import crypto from 'crypto';
import z from 'zod';

export const OAuth2OptionsSchema = z.object({
	metadataUri: z.string().url(),
	subjectClaim: z.string().optional().default('sub'),
});

export type OAuth2Options = z.infer<typeof OAuth2OptionsSchema>;

export function sha256(token: string): string {
	return crypto.createHash('sha256').update(token).digest('hex');
}
