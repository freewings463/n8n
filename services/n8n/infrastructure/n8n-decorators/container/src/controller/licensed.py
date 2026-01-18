"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/controller/licensed.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src/controller 的模块。导入/依赖:外部:无；内部:@n8n/constants、@n8n/di；本地:./controller-registry-metadata、./types。导出:Licensed。关键函数/方法:String。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/controller/licensed.ts -> services/n8n/infrastructure/n8n-decorators/container/src/controller/licensed.py

import type { BooleanLicenseFeature } from '@n8n/constants';
import { Container } from '@n8n/di';

import { ControllerRegistryMetadata } from './controller-registry-metadata';
import type { Controller } from './types';

export const Licensed =
	(licenseFeature: BooleanLicenseFeature): MethodDecorator =>
	(target, handlerName) => {
		const routeMetadata = Container.get(ControllerRegistryMetadata).getRouteMetadata(
			target.constructor as Controller,
			String(handlerName),
		);
		routeMetadata.licenseFeature = licenseFeature;
	};
