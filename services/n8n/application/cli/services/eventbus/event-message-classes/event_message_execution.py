"""
MIGRATION-META:
  source_path: packages/cli/src/eventbus/event-message-classes/event-message-execution.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/eventbus/event-message-classes 的执行模块。导入/依赖:外部:无；内部:n8n-workflow；本地:.、./abstract-event-message、./abstract-event-message-options、./abstract-event-payload。导出:EventPayloadExecution、EventMessageExecutionOptions、EventMessageExecution。关键函数/方法:setPayload、deserialize。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/eventbus/event-message-classes/event-message-execution.ts -> services/n8n/application/cli/services/eventbus/event-message-classes/event_message_execution.py

import type { JsonObject } from 'n8n-workflow';
import { EventMessageTypeNames } from 'n8n-workflow';

import type { EventNamesExecutionType } from '.';
import { AbstractEventMessage, isEventMessageOptionsWithType } from './abstract-event-message';
import type { AbstractEventMessageOptions } from './abstract-event-message-options';
import type { AbstractEventPayload } from './abstract-event-payload';

export interface EventPayloadExecution extends AbstractEventPayload {
	executionId: string;
}

export interface EventMessageExecutionOptions extends AbstractEventMessageOptions {
	eventName: EventNamesExecutionType;

	payload?: EventPayloadExecution;
}

export class EventMessageExecution extends AbstractEventMessage {
	readonly __type = EventMessageTypeNames.execution;

	eventName: EventNamesExecutionType;

	payload: EventPayloadExecution;

	constructor(options: EventMessageExecutionOptions) {
		super(options);
		if (options.payload) this.setPayload(options.payload);
		if (options.anonymize) {
			this.anonymize();
		}
	}

	setPayload(payload: EventPayloadExecution): this {
		this.payload = payload;
		return this;
	}

	deserialize(data: JsonObject): this {
		if (isEventMessageOptionsWithType(data, this.__type)) {
			this.setOptionsOrDefault(data);
			if (data.payload) this.setPayload(data.payload as EventPayloadExecution);
		}
		return this;
	}
}
