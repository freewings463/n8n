"""
MIGRATION-META:
  source_path: packages/workflow/src/errors/base/base.error.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/errors/base 的工作流错误。导入/依赖:外部:@sentry/node、callsites；内部:@n8n/errors；本地:无。导出:BaseErrorOptions。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Workflow errors -> domain/exceptions
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/errors/base/base.error.ts -> services/n8n/domain/workflow/exceptions/base/base_error.py

import type { Event } from '@sentry/node';
import callsites from 'callsites';

import type { ErrorTags, ErrorLevel, ReportingOptions } from '@n8n/errors';

export type BaseErrorOptions = { description?: string | undefined | null } & ErrorOptions &
	ReportingOptions;
/**
 * Base class for all errors
 */
export abstract class BaseError extends Error {
	/**
	 * Error level. Defines which level the error should be logged/reported
	 * @default 'error'
	 */
	level: ErrorLevel;

	/**
	 * Whether the error should be reported to Sentry.
	 * @default true
	 */
	readonly shouldReport: boolean;

	readonly description: string | null | undefined;

	readonly tags: ErrorTags;

	readonly extra?: Event['extra'];

	readonly packageName?: string;

	constructor(
		message: string,
		{
			level = 'error',
			description,
			shouldReport,
			tags = {},
			extra,
			...rest
		}: BaseErrorOptions = {},
	) {
		super(message, rest);

		this.level = level;
		this.shouldReport = shouldReport ?? (level === 'error' || level === 'fatal');
		this.description = description;
		this.tags = tags;
		this.extra = extra;

		try {
			const filePath = callsites()[2].getFileName() ?? '';
			const match = /packages\/([^\/]+)\//.exec(filePath)?.[1];

			if (match) this.tags.packageName = match;
		} catch {}
	}
}
