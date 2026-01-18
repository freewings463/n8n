"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/shutdown/shutdown-metadata.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/decorators/src/shutdown 的模块。导入/依赖:外部:无；内部:@n8n/di、n8n-workflow；本地:./constants、./types。导出:ShutdownMetadata。关键函数/方法:register、getHandlersByPriority、clear。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/shutdown/shutdown-metadata.ts -> services/n8n/application/n8n-decorators/services/shutdown/shutdown_metadata.py

import { Service } from '@n8n/di';
import { UserError } from 'n8n-workflow';

import { HIGHEST_SHUTDOWN_PRIORITY, LOWEST_SHUTDOWN_PRIORITY } from './constants';
import type { ShutdownHandler } from './types';

@Service()
export class ShutdownMetadata {
	private handlersByPriority: ShutdownHandler[][] = [];

	register(priority: number, handler: ShutdownHandler) {
		if (priority < LOWEST_SHUTDOWN_PRIORITY || priority > HIGHEST_SHUTDOWN_PRIORITY) {
			throw new UserError(
				`Invalid shutdown priority. Please set it between ${LOWEST_SHUTDOWN_PRIORITY} and ${HIGHEST_SHUTDOWN_PRIORITY}.`,
				{ extra: { priority } },
			);
		}

		if (!this.handlersByPriority[priority]) this.handlersByPriority[priority] = [];

		this.handlersByPriority[priority].push(handler);
	}

	getHandlersByPriority(): ShutdownHandler[][] {
		return this.handlersByPriority;
	}

	clear() {
		this.handlersByPriority = [];
	}
}
