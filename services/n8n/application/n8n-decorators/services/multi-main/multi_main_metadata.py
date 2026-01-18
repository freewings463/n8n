"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/multi-main/multi-main-metadata.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/decorators/src/multi-main 的模块。导入/依赖:外部:无；内部:@n8n/di；本地:../types。导出:LEADER_TAKEOVER_EVENT_NAME、LEADER_STEPDOWN_EVENT_NAME、MultiMainEvent、MultiMainMetadata。关键函数/方法:register、getHandlers。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/multi-main/multi-main-metadata.ts -> services/n8n/application/n8n-decorators/services/multi-main/multi_main_metadata.py

import { Service } from '@n8n/di';

import type { EventHandler } from '../types';

export const LEADER_TAKEOVER_EVENT_NAME = 'leader-takeover';
export const LEADER_STEPDOWN_EVENT_NAME = 'leader-stepdown';

export type MultiMainEvent = typeof LEADER_TAKEOVER_EVENT_NAME | typeof LEADER_STEPDOWN_EVENT_NAME;

type MultiMainEventHandler = EventHandler<MultiMainEvent>;

@Service()
export class MultiMainMetadata {
	private readonly handlers: MultiMainEventHandler[] = [];

	register(handler: MultiMainEventHandler) {
		this.handlers.push(handler);
	}

	getHandlers(): MultiMainEventHandler[] {
		return this.handlers;
	}
}
