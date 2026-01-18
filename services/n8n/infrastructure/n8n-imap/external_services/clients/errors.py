"""
MIGRATION-META:
  source_path: packages/@n8n/imap/src/errors.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/imap/src 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:ConnectionTimeoutError、ConnectionClosedError、ConnectionEndedError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/imap treated as external service client library
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/imap/src/errors.ts -> services/n8n/infrastructure/n8n-imap/external_services/clients/errors.py

export abstract class ImapError extends Error {}

/** Error thrown when a connection attempt has timed out */
export class ConnectionTimeoutError extends ImapError {
	constructor(
		/** timeout in milliseconds that the connection waited before timing out */
		readonly timeout?: number,
	) {
		let message = 'connection timed out';
		if (timeout) {
			message += `. timeout = ${timeout} ms`;
		}
		super(message);
	}
}

export class ConnectionClosedError extends ImapError {
	constructor() {
		super('Connection closed unexpectedly');
	}
}

export class ConnectionEndedError extends ImapError {
	constructor() {
		super('Connection ended unexpectedly');
	}
}
