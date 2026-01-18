"""
MIGRATION-META:
  source_path: packages/cli/src/errors/response-errors/too-many-requests.error.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/errors/response-errors 的错误。导入/依赖:外部:无；内部:无；本地:./abstract/response.error。导出:TooManyRequestsError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ResponseError (HTTP-mapped error)
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/errors/response-errors/too-many-requests.error.ts -> services/n8n/presentation/cli/api/errors/response-errors/too_many_requests_error.py

import { ResponseError } from './abstract/response.error';

export class TooManyRequestsError extends ResponseError {
	constructor(message: string, hint: string | undefined = undefined) {
		super(message, 429, 429, hint);
	}
}
