"""
MIGRATION-META:
  source_path: packages/workflow/src/errors/node-operation.error.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/errors 的工作流错误。导入/依赖:外部:无；内部:@n8n/errors；本地:./abstract/node.error、./node-api.error、../interfaces。导出:NodeOperationError。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Workflow errors -> domain/exceptions
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/errors/node-operation.error.ts -> services/n8n/domain/workflow/exceptions/node_operation_error.py

import { NodeError } from './abstract/node.error';
import { ApplicationError } from '@n8n/errors';
import type { NodeOperationErrorOptions } from './node-api.error';
import type { INode, JsonObject } from '../interfaces';

/**
 * Class for instantiating an operational error, e.g. an invalid credentials error.
 */
export class NodeOperationError extends NodeError {
	type: string | undefined;

	constructor(
		node: INode,
		error: Error | string | JsonObject,
		options: NodeOperationErrorOptions = {},
	) {
		if (error instanceof NodeOperationError) {
			return error;
		}

		if (typeof error === 'string') {
			error = new ApplicationError(error, { level: options.level ?? 'warning' });
		}

		super(node, error);

		if (error instanceof NodeError && error?.messages?.length) {
			error.messages.forEach((message) => this.addToMessages(message));
		}

		if (options.message) this.message = options.message;
		this.level = options.level ?? 'warning';
		if (options.functionality) this.functionality = options.functionality;
		if (options.type) this.type = options.type;

		if (options.description) this.description = options.description;
		else if ('description' in error && typeof error.description === 'string')
			this.description = error.description;

		this.context.runIndex = options.runIndex;
		this.context.itemIndex = options.itemIndex;
		this.context.metadata = options.metadata;

		if (this.message === this.description) {
			this.description = undefined;
		}

		[this.message, this.messages] = this.setDescriptiveErrorMessage(
			this.message,
			this.messages,
			undefined,
			options.messageMapping,
		);
	}
}
