"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/controller/scoped.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src/controller 的模块。导入/依赖:外部:无；内部:@n8n/di、@n8n/permissions；本地:./controller-registry-metadata、./types。导出:GlobalScope、ProjectScope。关键函数/方法:String、GlobalScope、ProjectScope。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/controller/scoped.ts -> services/n8n/infrastructure/n8n-decorators/container/src/controller/scoped.py

import { Container } from '@n8n/di';
import type { Scope } from '@n8n/permissions';

import { ControllerRegistryMetadata } from './controller-registry-metadata';
import type { Controller } from './types';

const Scoped =
	(scope: Scope, { globalOnly } = { globalOnly: false }): MethodDecorator =>
	(target, handlerName) => {
		const routeMetadata = Container.get(ControllerRegistryMetadata).getRouteMetadata(
			target.constructor as Controller,
			String(handlerName),
		);
		routeMetadata.accessScope = { scope, globalOnly };
	};

/**
 * Decorator for a controller method to ensure the user has a scope,
 * checking only at the global level.
 *
 * To check only at project level as well, use the `@ProjectScope` decorator.
 *
 * @example
 * ```ts
 * @RestController()
 * export class UsersController {
 *   @Delete('/:id')
 *   @GlobalScope('user:delete')
 *   async deleteUser(req, res) { ... }
 * }
 * ```
 */
export const GlobalScope = (scope: Scope) => Scoped(scope, { globalOnly: true });

/**
 * Decorator for a controller method to ensure the user has a scope,
 * checking first at project level and then at global level.
 *
 * To check only at global level, use the `@GlobalScope` decorator.
 *
 * @example
 * ```ts
 * @RestController()
 * export class WorkflowController {
 *   @Get('/:workflowId')
 *   @GlobalScope('workflow:read')
 *   async getWorkflow(req, res) { ... }
 * }
 * ```
 */

export const ProjectScope = (scope: Scope) => Scoped(scope);
