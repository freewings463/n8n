"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/controller/middleware.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src/controller 的中间件。导入/依赖:外部:无；内部:@n8n/di；本地:./controller-registry-metadata、./types。导出:Middleware。关键函数/方法:Middleware。用于为该模块提供鉴权、拦截、上下文或统一异常处理。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/controller/middleware.ts -> services/n8n/infrastructure/n8n-decorators/container/src/controller/middleware.py

import { Container } from '@n8n/di';

import { ControllerRegistryMetadata } from './controller-registry-metadata';
import type { Controller } from './types';

export const Middleware = (): MethodDecorator => (target, handlerName) => {
	const metadata = Container.get(ControllerRegistryMetadata).getControllerMetadata(
		target.constructor as Controller,
	);
	metadata.middlewares.push(String(handlerName));
};
