"""
MIGRATION-META:
  source_path: packages/workflow/src/errors/workflow-activation.error.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src/errors 的工作流错误。导入/依赖:外部:无；内部:@n8n/errors；本地:./abstract/execution-base.error、../interfaces。导出:WorkflowActivationError。关键函数/方法:setLevel。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Workflow errors -> domain/exceptions
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/errors/workflow-activation.error.ts -> services/n8n/domain/workflow/exceptions/workflow_activation_error.py

import { ExecutionBaseError } from './abstract/execution-base.error';
import type { ApplicationError } from '@n8n/errors';
import type { INode } from '../interfaces';

interface WorkflowActivationErrorOptions {
	cause?: Error;
	node?: INode;
	level?: ApplicationError['level'];
	workflowId?: string;
}

/**
 * Class for instantiating an workflow activation error
 */
export class WorkflowActivationError extends ExecutionBaseError {
	node: INode | undefined;

	workflowId: string | undefined;

	constructor(
		message: string,
		{ cause, node, level, workflowId }: WorkflowActivationErrorOptions = {},
	) {
		let error = cause as Error;
		if (cause instanceof ExecutionBaseError) {
			error = new Error(cause.message);
			error.constructor = cause.constructor;
			error.name = cause.name;
			error.stack = cause.stack;
		}
		super(message, { cause: error });
		this.node = node;
		this.workflowId = workflowId;
		this.message = message;
		this.setLevel(level);
	}

	private setLevel(level?: ApplicationError['level']) {
		if (level) {
			this.level = level;
			return;
		}

		if (
			[
				'etimedout', // Node.js
				'econnrefused', // Node.js
				'eauth', // OAuth
				'temporary authentication failure', // IMAP server
				'invalid credentials',
			].some((str) => this.message.toLowerCase().includes(str))
		) {
			this.level = 'warning';
			return;
		}

		this.level = 'error';
	}
}
