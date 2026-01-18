"""
MIGRATION-META:
  source_path: packages/@n8n/errors/src/types.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/@n8n/errors/src 的类型。导入/依赖:外部:@sentry/node；内部:无；本地:无。导出:ErrorLevel、ErrorTags、ReportingOptions。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Shared error types -> domain/exceptions
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/errors/src/types.ts -> services/n8n/domain/n8n-errors/exceptions/types.py

import type { Event } from '@sentry/node';

export type ErrorLevel = 'fatal' | 'error' | 'warning' | 'info';

export type ErrorTags = NonNullable<Event['tags']>;

export type ReportingOptions = {
	/** Whether the error should be reported to Sentry */
	shouldReport?: boolean;
	/** Whether the error log should be logged (default to true) */
	shouldBeLogged?: boolean;
	level?: ErrorLevel;
	tags?: ErrorTags;
	extra?: Event['extra'];
	executionId?: string;
};
