"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Code/errors/WrappedExecutionError.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Code/errors 的执行节点。导入/依赖:外部:无；内部:@n8n/errors；本地:无。导出:WrappableError、WrappedExecutionError、isWrappableError。关键函数/方法:copyErrorProperties、isWrappableError。用于实现 n8n 执行节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Code/errors/WrappedExecutionError.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Code/errors/WrappedExecutionError.py

import { ApplicationError } from '@n8n/errors';

export type WrappableError = Record<string, unknown>;

/**
 * Errors received from the task runner are not instances of Error.
 * This class wraps them in an Error instance and makes all their
 * properties available.
 */
export class WrappedExecutionError extends ApplicationError {
	[key: string]: unknown;

	constructor(error: WrappableError) {
		const message = typeof error.message === 'string' ? error.message : 'Unknown error';
		super(message, {
			cause: error,
		});

		this.copyErrorProperties(error);
	}

	private copyErrorProperties(error: WrappableError) {
		for (const key of Object.getOwnPropertyNames(error)) {
			this[key] = error[key];
		}
	}
}

export function isWrappableError(error: unknown): error is WrappableError {
	return typeof error === 'object' && error !== null;
}
