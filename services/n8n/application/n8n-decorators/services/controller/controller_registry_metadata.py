"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/controller/controller-registry-metadata.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/decorators/src/controller 的模块。导入/依赖:外部:无；内部:@n8n/di；本地:./types。导出:ControllerRegistryMetadata。关键函数/方法:getControllerMetadata、getRouteMetadata。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/controller/controller-registry-metadata.ts -> services/n8n/application/n8n-decorators/services/controller/controller_registry_metadata.py

import { Service } from '@n8n/di';

import type { Controller, ControllerMetadata, HandlerName, RouteMetadata } from './types';

@Service()
export class ControllerRegistryMetadata {
	private registry = new Map<Controller, ControllerMetadata>();

	getControllerMetadata(controllerClass: Controller) {
		let metadata = this.registry.get(controllerClass);
		if (!metadata) {
			metadata = {
				basePath: '/',
				registerOnRootPath: false,
				middlewares: [],
				routes: new Map(),
			};
			this.registry.set(controllerClass, metadata);
		}
		return metadata;
	}

	getRouteMetadata(controllerClass: Controller, handlerName: HandlerName) {
		const metadata = this.getControllerMetadata(controllerClass);
		let route = metadata.routes.get(handlerName);
		if (!route) {
			route = {} as RouteMetadata;
			route.args = [];
			metadata.routes.set(handlerName, route);
		}
		return route;
	}

	get controllerClasses() {
		return this.registry.keys();
	}
}
