"""
MIGRATION-META:
  source_path: packages/@n8n/syslog-client/src/errors.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/syslog-client/src 的模块。导入/依赖:外部:zod；内部:无；本地:无。导出:SyslogClientError、ValidationError、ConnectionError、TransportError、TimeoutError。关键函数/方法:fromZod。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/syslog-client treated as external service client library
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/syslog-client/src/errors.ts -> services/n8n/infrastructure/n8n-syslog-client/external_services/clients/errors.py

import type { ZodIssue } from 'zod';

/**
 * Base error class for all syslog client errors.
 * Extends native Error with additional context.
 */
export class SyslogClientError extends Error {
	constructor(
		message: string,
		readonly code?: string,
		readonly cause?: Error,
	) {
		super(message);
		this.name = 'SyslogClientError';

		// Maintain proper prototype chain for instanceof checks
		Object.setPrototypeOf(this, SyslogClientError.prototype);

		// Capture stack trace, excluding constructor call from it
		if (Error.captureStackTrace) {
			Error.captureStackTrace(this, this.constructor);
		}
	}
}

/**
 * Error thrown when client options validation fails.
 */
export class ValidationError extends SyslogClientError {
	constructor(
		message: string,
		readonly validationErrors: Array<{ path: string; message: string }>,
	) {
		super(message, 'VALIDATION_ERROR');
		this.name = 'ValidationError';
		Object.setPrototypeOf(this, ValidationError.prototype);
	}

	static fromZod(message: string, zodErrors: ZodIssue[]) {
		const errors = zodErrors.map((zodError) => ({
			path: zodError.path.join('.'),
			message: zodError.message,
		}));

		return new ValidationError(message, errors);
	}
}

/**
 * Error thrown when transport connection fails.
 */
export class ConnectionError extends SyslogClientError {
	constructor(message: string, cause?: Error) {
		super(message, 'CONNECTION_ERROR', cause);
		this.name = 'ConnectionError';
		Object.setPrototypeOf(this, ConnectionError.prototype);
	}
}

/**
 * Error thrown when transport operations fail (send/write).
 */
export class TransportError extends SyslogClientError {
	constructor(
		message: string,
		readonly transportType: string,
		cause?: Error,
	) {
		super(message, 'TRANSPORT_ERROR', cause);
		this.name = 'TransportError';
		Object.setPrototypeOf(this, TransportError.prototype);
	}
}

/**
 * Error thrown when timeout occurs.
 */
export class TimeoutError extends SyslogClientError {
	constructor(message: string = 'Connection timed out') {
		super(message, 'TIMEOUT_ERROR');
		this.name = 'TimeoutError';
		Object.setPrototypeOf(this, TimeoutError.prototype);
	}
}
