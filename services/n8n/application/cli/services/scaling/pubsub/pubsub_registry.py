"""
MIGRATION-META:
  source_path: packages/cli/src/scaling/pubsub/pubsub.registry.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/scaling/pubsub 的模块。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/decorators、@n8n/di、n8n-core；本地:./pubsub.eventbus。导出:PubSubRegistry。关键函数/方法:init、eventHandler。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/scaling/pubsub/pubsub.registry.ts -> services/n8n/application/cli/services/scaling/pubsub/pubsub_registry.py

import { Logger } from '@n8n/backend-common';
import { PubSubEventName, PubSubMetadata } from '@n8n/decorators';
import { Container, Service } from '@n8n/di';
import { InstanceSettings } from 'n8n-core';

import { PubSubEventBus } from './pubsub.eventbus';

@Service()
export class PubSubRegistry {
	constructor(
		private readonly logger: Logger,
		private readonly instanceSettings: InstanceSettings,
		private readonly pubSubMetadata: PubSubMetadata,
		private readonly pubsubEventBus: PubSubEventBus,
	) {
		this.logger = this.logger.scoped('pubsub');
	}

	private eventHandlers: Array<{
		eventName: PubSubEventName;
		handler: Parameters<PubSubEventBus['on']>[1];
	}> = [];

	init() {
		const { instanceSettings, pubSubMetadata } = this;
		// We clear the event handlers before registering new ones
		for (const { eventName, handler } of this.eventHandlers) {
			this.pubsubEventBus.off(eventName, handler);
		}
		this.eventHandlers = [];

		// Register all event handlers that match the current instance type and role
		const handlers = pubSubMetadata.getHandlers();
		for (const { eventHandlerClass, methodName, eventName, filter } of handlers) {
			const handlerClass = Container.get(eventHandlerClass);
			if (!filter?.instanceType || filter.instanceType === instanceSettings.instanceType) {
				this.logger.debug(
					`Registered a "${eventName}" event handler on ${eventHandlerClass.name}#${methodName}`,
				);
				const eventHandler = async (...args: unknown[]) => {
					// Since the instance role can change, this check needs to be in the event listener
					const shouldTrigger =
						filter?.instanceType !== 'main' ||
						!filter.instanceRole ||
						filter.instanceRole === instanceSettings.instanceRole;
					if (shouldTrigger) await handlerClass[methodName].call(handlerClass, ...args);
				};
				this.pubsubEventBus.on(eventName, eventHandler);
				this.eventHandlers.push({ eventName, handler: eventHandler });
			}
		}
	}
}
