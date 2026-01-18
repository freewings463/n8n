"""
MIGRATION-META:
  source_path: packages/workflow/src/errors/expression.error.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/errors 的工作流错误。导入/依赖:外部:无；内部:无；本地:../interfaces、./abstract/execution-base.error。导出:ExpressionErrorOptions、ExpressionError。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Workflow errors -> domain/exceptions
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/errors/expression.error.ts -> services/n8n/domain/workflow/exceptions/expression_error.py

import type { IDataObject } from '../interfaces';
import { ExecutionBaseError } from './abstract/execution-base.error';

export interface ExpressionErrorOptions {
	cause?: Error;
	causeDetailed?: string;
	description?: string;
	descriptionKey?: string;
	descriptionTemplate?: string;
	functionality?: 'pairedItem';
	itemIndex?: number;
	messageTemplate?: string;
	nodeCause?: string;
	parameter?: string;
	runIndex?: number;
	type?:
		| 'no_execution_data'
		| 'no_node_execution_data'
		| 'no_input_connection'
		| 'internal'
		| 'paired_item_invalid_info'
		| 'paired_item_no_info'
		| 'paired_item_multiple_matches'
		| 'paired_item_no_connection'
		| 'paired_item_intermediate_nodes';
}

/**
 * Class for instantiating an expression error
 */
export class ExpressionError extends ExecutionBaseError {
	constructor(message: string, options?: ExpressionErrorOptions) {
		super(message, { cause: options?.cause, level: 'warning' });

		if (options?.description !== undefined) {
			this.description = options.description;
		}

		const allowedKeys = [
			'causeDetailed',
			'descriptionTemplate',
			'descriptionKey',
			'itemIndex',
			'messageTemplate',
			'nodeCause',
			'parameter',
			'runIndex',
			'type',
		];

		if (options !== undefined) {
			if (options.functionality !== undefined) {
				this.functionality = options.functionality;
			}

			Object.keys(options as IDataObject).forEach((key) => {
				if (allowedKeys.includes(key)) {
					this.context[key] = (options as IDataObject)[key];
				}
			});
		}
	}
}
