"""
MIGRATION-META:
  source_path: packages/@n8n/task-runner/src/js-task-runner/require-resolver.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/task-runner/src/js-task-runner 的模块。导入/依赖:外部:node:module；内部:无；本地:./errors/disallowed-module.error、./errors/execution-error。导出:RequireResolverOpts、RequireResolver、createRequireResolver。关键函数/方法:createRequireResolver、checkIsAllowed。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Task runner process runtime -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/task-runner/src/js-task-runner/require-resolver.ts -> services/n8n/infrastructure/n8n-task-runner/container/js-task-runner/require_resolver.py

import { isBuiltin } from 'node:module';

import { DisallowedModuleError } from './errors/disallowed-module.error';
import { ExecutionError } from './errors/execution-error';

export type RequireResolverOpts = {
	/**
	 * List of built-in nodejs modules that are allowed to be required in the
	 * execution sandbox. `"*"` means all are allowed.
	 */
	allowedBuiltInModules: Set<string> | '*';

	/**
	 * List of external modules that are allowed to be required in the
	 * execution sandbox. `"*"` means all are allowed.
	 */
	allowedExternalModules: Set<string> | '*';
};

export type RequireResolver = (request: string) => unknown;

export function createRequireResolver({
	allowedBuiltInModules,
	allowedExternalModules,
}: RequireResolverOpts) {
	return (request: string) => {
		const checkIsAllowed = (allowList: Set<string> | '*', moduleName: string) => {
			return allowList === '*' || allowList.has(moduleName);
		};

		const isAllowed = isBuiltin(request)
			? checkIsAllowed(allowedBuiltInModules, request)
			: checkIsAllowed(allowedExternalModules, request);

		if (!isAllowed) {
			const error = new DisallowedModuleError(request);
			throw new ExecutionError(error);
		}

		return require(request) as unknown;
	};
}
