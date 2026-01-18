"""
MIGRATION-META:
  source_path: packages/@n8n/errors/src/application.error.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/errors/src 的错误。导入/依赖:外部:@sentry/node、callsites；内部:无；本地:./types。导出:ApplicationError。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Shared error types -> domain/exceptions
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/errors/src/application.error.ts -> services/n8n/domain/n8n-errors/exceptions/application_error.py

import type { Event } from '@sentry/node';
import callsites from 'callsites';

import type { ErrorLevel, ReportingOptions } from './types';

/**
 * @deprecated Use `UserError`, `OperationalError` or `UnexpectedError` instead.
 */
export class ApplicationError extends Error {
	level: ErrorLevel;

	readonly tags: NonNullable<Event['tags']>;

	readonly extra?: Event['extra'];

	readonly packageName?: string;

	constructor(
		message: string,
		{ level, tags = {}, extra, ...rest }: ErrorOptions & ReportingOptions = {},
	) {
		super(message, rest);
		this.level = level ?? 'error';
		this.tags = tags;
		this.extra = extra;

		try {
			const filePath = callsites()[2].getFileName() ?? '';
			// eslint-disable-next-line no-useless-escape
			const match = /packages\/([^\/]+)\//.exec(filePath)?.[1];

			if (match) this.tags.packageName = match;
			// eslint-disable-next-line no-empty
		} catch {}
	}
}
