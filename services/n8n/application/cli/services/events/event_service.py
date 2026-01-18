"""
MIGRATION-META:
  source_path: packages/cli/src/events/event.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/events 的服务。导入/依赖:外部:无；内部:@n8n/di、@/typed-emitter；本地:./maps/ai.event-map、./maps/queue-metrics.event-map、./maps/relay.event-map。导出:EventService。关键函数/方法:无。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/events/event.service.ts -> services/n8n/application/cli/services/events/event_service.py

import { Service } from '@n8n/di';

import { TypedEmitter } from '@/typed-emitter';

import type { AiEventMap } from './maps/ai.event-map';
import type { QueueMetricsEventMap } from './maps/queue-metrics.event-map';
import type { RelayEventMap } from './maps/relay.event-map';

type EventMap = RelayEventMap & QueueMetricsEventMap & AiEventMap;

@Service()
export class EventService extends TypedEmitter<EventMap> {}
