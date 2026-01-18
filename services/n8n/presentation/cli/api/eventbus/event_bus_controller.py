"""
MIGRATION-META:
  source_path: packages/cli/src/eventbus/event-bus.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/eventbus 的控制器。导入/依赖:外部:express；内部:@n8n/db、@n8n/decorators 等2项；本地:./event-message-classes、./message-event-bus/message-event-bus 等2项。导出:EventBusController。关键函数/方法:isWithIdString、isMessageEventBusDestinationWebhookOptions、isMessageEventBusDestinationOptions、getEventNames、getDestination、postDestination、sendTestMessage、deleteDestination。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/eventbus/event-bus.controller.ts -> services/n8n/presentation/cli/api/eventbus/event_bus_controller.py

import { AuthenticatedRequest } from '@n8n/db';
import { RestController, Get, Post, Delete, GlobalScope, Licensed } from '@n8n/decorators';
import express from 'express';
import type {
	MessageEventBusDestinationWebhookOptions,
	MessageEventBusDestinationOptions,
} from 'n8n-workflow';
import { MessageEventBusDestinationTypeNames } from 'n8n-workflow';

import { BadRequestError } from '@/errors/response-errors/bad-request.error';

import { eventNamesAll } from './event-message-classes';
import { MessageEventBus } from './message-event-bus/message-event-bus';
import {
	isMessageEventBusDestinationSentryOptions,
	MessageEventBusDestinationSentry,
} from './message-event-bus-destination/message-event-bus-destination-sentry.ee';
import {
	isMessageEventBusDestinationSyslogOptions,
	MessageEventBusDestinationSyslog,
} from './message-event-bus-destination/message-event-bus-destination-syslog.ee';
import { MessageEventBusDestinationWebhook } from './message-event-bus-destination/message-event-bus-destination-webhook.ee';
import type { MessageEventBusDestination } from './message-event-bus-destination/message-event-bus-destination.ee';

const isWithIdString = (candidate: unknown): candidate is { id: string } => {
	const o = candidate as { id: string };
	if (!o) return false;
	return o.id !== undefined;
};

const isMessageEventBusDestinationWebhookOptions = (
	candidate: unknown,
): candidate is MessageEventBusDestinationWebhookOptions => {
	const o = candidate as MessageEventBusDestinationWebhookOptions;
	if (!o) return false;
	return o.url !== undefined;
};

const isMessageEventBusDestinationOptions = (
	candidate: unknown,
): candidate is MessageEventBusDestinationOptions => {
	const o = candidate as MessageEventBusDestinationOptions;
	if (!o) return false;
	return o.__type !== undefined;
};

@RestController('/eventbus')
export class EventBusController {
	constructor(private readonly eventBus: MessageEventBus) {}

	@Get('/eventnames')
	async getEventNames(): Promise<string[]> {
		return eventNamesAll;
	}

	@Licensed('feat:logStreaming')
	@Get('/destination')
	@GlobalScope('eventBusDestination:list')
	async getDestination(req: express.Request): Promise<MessageEventBusDestinationOptions[]> {
		if (isWithIdString(req.query)) {
			return await this.eventBus.findDestination(req.query.id);
		} else {
			return await this.eventBus.findDestination();
		}
	}

	@Licensed('feat:logStreaming')
	@Post('/destination')
	@GlobalScope('eventBusDestination:create')
	async postDestination(req: AuthenticatedRequest): Promise<any> {
		let result: MessageEventBusDestination | undefined;
		if (isMessageEventBusDestinationOptions(req.body)) {
			switch (req.body.__type) {
				case MessageEventBusDestinationTypeNames.sentry:
					if (isMessageEventBusDestinationSentryOptions(req.body)) {
						result = await this.eventBus.addDestination(
							new MessageEventBusDestinationSentry(this.eventBus, req.body),
						);
					}
					break;
				case MessageEventBusDestinationTypeNames.webhook:
					if (isMessageEventBusDestinationWebhookOptions(req.body)) {
						result = await this.eventBus.addDestination(
							new MessageEventBusDestinationWebhook(this.eventBus, req.body),
						);
					}
					break;
				case MessageEventBusDestinationTypeNames.syslog:
					if (isMessageEventBusDestinationSyslogOptions(req.body)) {
						result = await this.eventBus.addDestination(
							new MessageEventBusDestinationSyslog(this.eventBus, req.body),
						);
					}
					break;
				default:
					throw new BadRequestError(
						`Body is missing ${req.body.__type} options or type ${req.body.__type} is unknown`,
					);
			}
			if (result) {
				await result.saveToDb();
				return {
					...result.serialize(),
					eventBusInstance: undefined,
				};
			}
			throw new BadRequestError('There was an error adding the destination');
		}
		throw new BadRequestError('Body is not configuring MessageEventBusDestinationOptions');
	}

	@Licensed('feat:logStreaming')
	@Get('/testmessage')
	@GlobalScope('eventBusDestination:test')
	async sendTestMessage(req: express.Request): Promise<boolean> {
		if (isWithIdString(req.query)) {
			return await this.eventBus.testDestination(req.query.id);
		}
		return false;
	}

	@Licensed('feat:logStreaming')
	@Delete('/destination')
	@GlobalScope('eventBusDestination:delete')
	async deleteDestination(req: AuthenticatedRequest) {
		if (isWithIdString(req.query)) {
			await this.eventBus.removeDestination(req.query.id);
			return await this.eventBus.deleteDestination(req.query.id);
		} else {
			throw new BadRequestError('Query is missing id');
		}
	}
}
