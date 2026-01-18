"""
MIGRATION-META:
  source_path: packages/cli/src/errors/response-errors/abstract/response.error.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/errors/response-errors/abstract 的错误。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected ResponseError (HTTP-mapped error)
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/errors/response-errors/abstract/response.error.ts -> services/n8n/presentation/cli/api/errors/response-errors/abstract/response_error.py

import { BaseError } from 'n8n-workflow';

/**
 * Special Error which allows to return also an error code and http status code
 */
export abstract class ResponseError extends BaseError {
	/**
	 * Optional metadata to be included in the error response.
	 * This allows errors to include additional structured data beyond the standard
	 * message, code, and hint fields. For example, LicenseEulaRequiredError uses
	 * this to include the EULA URL that must be accepted.
	 */
	readonly meta?: Record<string, unknown>;

	/**
	 * Creates an instance of ResponseError.
	 * Must be used inside a block with `ResponseHelper.send()`.
	 */
	constructor(
		message: string,
		// The HTTP status code of  response
		readonly httpStatusCode: number,
		// The error code in the response
		readonly errorCode: number = httpStatusCode,
		// The error hint the response
		readonly hint: string | undefined = undefined,
		cause?: unknown,
	) {
		super(message, { cause });
		this.name = 'ResponseError';

		if (httpStatusCode >= 400 && httpStatusCode < 500) {
			this.level = 'warning'; // client errors (4xx)
		} else if (httpStatusCode >= 502 && httpStatusCode <= 504) {
			this.level = 'info'; // transient errors (502, 503, 504)
		} else {
			this.level = 'error'; // other 5xx
		}
	}
}
