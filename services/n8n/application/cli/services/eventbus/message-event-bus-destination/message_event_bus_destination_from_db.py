"""
MIGRATION-META:
  source_path: packages/cli/src/eventbus/message-event-bus-destination/message-event-bus-destination-from-db.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/eventbus/message-event-bus-destination 的模块。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/db、@n8n/di、n8n-workflow；本地:./message-event-bus-destination-sentry.ee、./message-event-bus-destination-syslog.ee、./message-event-bus-destination-webhook.ee、./message-event-bus-destination.ee 等1项。导出:messageEventBusDestinationFromDb。关键函数/方法:messageEventBusDestinationFromDb。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/eventbus/message-event-bus-destination/message-event-bus-destination-from-db.ts -> services/n8n/application/cli/services/eventbus/message-event-bus-destination/message_event_bus_destination_from_db.py

import { Logger } from '@n8n/backend-common';
import type { EventDestinations } from '@n8n/db';
import { Container } from '@n8n/di';
import { MessageEventBusDestinationTypeNames } from 'n8n-workflow';

import { MessageEventBusDestinationSentry } from './message-event-bus-destination-sentry.ee';
import { MessageEventBusDestinationSyslog } from './message-event-bus-destination-syslog.ee';
import { MessageEventBusDestinationWebhook } from './message-event-bus-destination-webhook.ee';
import type { MessageEventBusDestination } from './message-event-bus-destination.ee';
import type { MessageEventBus } from '../message-event-bus/message-event-bus';

export function messageEventBusDestinationFromDb(
	eventBusInstance: MessageEventBus,
	dbData: EventDestinations,
): MessageEventBusDestination | null {
	const destinationData = dbData.destination;
	if ('__type' in destinationData) {
		switch (destinationData.__type) {
			case MessageEventBusDestinationTypeNames.sentry:
				return MessageEventBusDestinationSentry.deserialize(eventBusInstance, destinationData);
			case MessageEventBusDestinationTypeNames.syslog:
				return MessageEventBusDestinationSyslog.deserialize(eventBusInstance, destinationData);
			case MessageEventBusDestinationTypeNames.webhook:
				return MessageEventBusDestinationWebhook.deserialize(eventBusInstance, destinationData);
			default:
				Container.get(Logger).debug('MessageEventBusDestination __type unknown');
		}
	}
	return null;
}
