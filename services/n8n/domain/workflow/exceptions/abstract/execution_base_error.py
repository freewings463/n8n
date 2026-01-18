"""
MIGRATION-META:
  source_path: packages/workflow/src/errors/abstract/execution-base.error.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/errors/abstract 的工作流错误。导入/依赖:外部:无；内部:@n8n/errors；本地:../../interfaces。导出:无。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Workflow errors -> domain/exceptions
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/errors/abstract/execution-base.error.ts -> services/n8n/domain/workflow/exceptions/abstract/execution_base_error.py

import { ApplicationError, type ReportingOptions } from '@n8n/errors';

import type { Functionality, IDataObject, JsonObject } from '../../interfaces';

interface ExecutionBaseErrorOptions extends ReportingOptions {
	cause?: Error;
	errorResponse?: JsonObject;
}

export abstract class ExecutionBaseError extends ApplicationError {
	description: string | null | undefined;

	override cause?: Error;

	errorResponse?: JsonObject;

	timestamp: number;

	context: IDataObject = {};

	lineNumber: number | undefined;

	functionality: Functionality = 'regular';

	constructor(message: string, options: ExecutionBaseErrorOptions = {}) {
		super(message, options);

		this.name = this.constructor.name;
		this.timestamp = Date.now();

		const { cause, errorResponse } = options;
		if (cause instanceof ExecutionBaseError) {
			this.context = cause.context;
		} else if (cause && !(cause instanceof Error)) {
			this.cause = cause;
		}

		if (errorResponse) this.errorResponse = errorResponse;
	}

	toJSON?() {
		return {
			message: this.message,
			lineNumber: this.lineNumber,
			timestamp: this.timestamp,
			name: this.name,
			description: this.description,
			context: this.context,
			cause: this.cause,
		};
	}
}
