"""
MIGRATION-META:
  source_path: packages/cli/src/events/relays/event-relay.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/events/relays 的模块。导入/依赖:外部:无；内部:@n8n/di、@/events/event.service、@/events/…/relay.event-map；本地:无。导出:EventRelay。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/events/relays/event-relay.ts -> services/n8n/application/cli/services/events/relays/event_relay.py

import { Service } from '@n8n/di';

import { EventService } from '@/events/event.service';
import type { RelayEventMap } from '@/events/maps/relay.event-map';

@Service()
export class EventRelay {
	constructor(readonly eventService: EventService) {}

	protected setupListeners<EventNames extends keyof RelayEventMap>(
		map: {
			[EventName in EventNames]?: (event: RelayEventMap[EventName]) => void | Promise<void>;
		},
	) {
		for (const [eventName, handler] of Object.entries(map) as Array<
			[EventNames, (event: RelayEventMap[EventNames]) => void | Promise<void>]
		>) {
			this.eventService.on(eventName, async (event) => {
				await handler(event);
			});
		}
	}
}
