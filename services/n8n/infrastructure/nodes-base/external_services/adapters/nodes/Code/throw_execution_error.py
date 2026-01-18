"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Code/throw-execution-error.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Code 的执行节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./errors/WrappedExecutionError。导出:throwExecutionError。关键函数/方法:throwExecutionError。用于实现 n8n 执行节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Code/throw-execution-error.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Code/throw_execution_error.py

import { ApplicationError } from 'n8n-workflow';

import { isWrappableError, WrappedExecutionError } from './errors/WrappedExecutionError';

export function throwExecutionError(error: unknown): never {
	if (error instanceof Error) {
		throw error;
	} else if (isWrappableError(error)) {
		// The error coming from task runner is not an instance of error,
		// so we need to wrap it in an error instance.
		throw new WrappedExecutionError(error);
	}

	throw new ApplicationError(`Unknown error: ${JSON.stringify(error)}`);
}
