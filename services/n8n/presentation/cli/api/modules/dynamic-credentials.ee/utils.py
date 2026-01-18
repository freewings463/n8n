"""
MIGRATION-META:
  source_path: packages/cli/src/modules/dynamic-credentials.ee/utils.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/dynamic-credentials.ee 的模块。导入/依赖:外部:express；内部:@/errors/…/bad-request.error、@/errors/…/unauthenticated.error；本地:无。导出:getBearerToken。关键函数/方法:getBearerToken。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/dynamic-credentials.ee/utils.ts -> services/n8n/presentation/cli/api/modules/dynamic-credentials.ee/utils.py

import { BadRequestError } from '@/errors/response-errors/bad-request.error';
import { UnauthenticatedError } from '@/errors/response-errors/unauthenticated.error';
import type { Request } from 'express';

const BEARER_TOKEN_REGEX = /^[Bb][Ee][Aa][Rr][Ee][Rr]\s+(.+)$/;

export function getBearerToken(req: Request): string {
	const headerValue = req.headers['authorization']?.toString();

	if (!headerValue) {
		throw new UnauthenticatedError();
	}

	const result = BEARER_TOKEN_REGEX.exec(headerValue);
	const token = result ? result[1] : null;

	if (!token) {
		throw new BadRequestError('Authorization header is malformed');
	}

	return token;
}
