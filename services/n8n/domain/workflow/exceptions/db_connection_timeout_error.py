"""
MIGRATION-META:
  source_path: packages/workflow/src/errors/db-connection-timeout-error.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/errors 的工作流错误。导入/依赖:外部:无；内部:@n8n/errors；本地:无。导出:DbConnectionTimeoutErrorOpts、DbConnectionTimeoutError。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Workflow errors -> domain/exceptions
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/errors/db-connection-timeout-error.ts -> services/n8n/domain/workflow/exceptions/db_connection_timeout_error.py

import { ApplicationError } from '@n8n/errors';

export type DbConnectionTimeoutErrorOpts = {
	configuredTimeoutInMs: number;
	cause: Error;
};

export class DbConnectionTimeoutError extends ApplicationError {
	constructor(opts: DbConnectionTimeoutErrorOpts) {
		const numberFormat = Intl.NumberFormat();
		const errorMessage = `Could not establish database connection within the configured timeout of ${numberFormat.format(opts.configuredTimeoutInMs)} ms. Please ensure the database is configured correctly and the server is reachable. You can increase the timeout by setting the 'DB_POSTGRESDB_CONNECTION_TIMEOUT' environment variable.`;
		super(errorMessage, { cause: opts.cause });
	}
}
