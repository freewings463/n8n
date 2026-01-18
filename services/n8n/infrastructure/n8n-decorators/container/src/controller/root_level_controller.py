"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/controller/root-level-controller.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src/controller 的控制器。导入/依赖:外部:无；内部:@n8n/di；本地:./controller-registry-metadata、./types。导出:RootLevelController。关键函数/方法:无。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/controller/root-level-controller.ts -> services/n8n/infrastructure/n8n-decorators/container/src/controller/root_level_controller.py

import { Container, Service } from '@n8n/di';

import { ControllerRegistryMetadata } from './controller-registry-metadata';
import type { Controller } from './types';

/**
 * Defines a controller that should be registered on the root path, without any prefix
 * @param basePath defaults to `/`
 * @returns ClassDecorator
 */
export const RootLevelController =
	(basePath: `/${string}` = '/'): ClassDecorator =>
	(target) => {
		const metadata = Container.get(ControllerRegistryMetadata).getControllerMetadata(
			target as unknown as Controller,
		);
		metadata.basePath = basePath;
		metadata.registerOnRootPath = true;
		// eslint-disable-next-line @typescript-eslint/no-unsafe-return
		return Service()(target);
	};
