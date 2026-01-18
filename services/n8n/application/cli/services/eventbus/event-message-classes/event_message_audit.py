"""
MIGRATION-META:
  source_path: packages/cli/src/eventbus/event-message-classes/event-message-audit.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/eventbus/event-message-classes 的模块。导入/依赖:外部:无；内部:n8n-workflow；本地:.、./abstract-event-message、./abstract-event-message-options、./abstract-event-payload。导出:EventPayloadAudit、EventMessageAuditOptions、EventMessageAudit。关键函数/方法:setPayload、deserialize。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/eventbus/event-message-classes/event-message-audit.ts -> services/n8n/application/cli/services/eventbus/event-message-classes/event_message_audit.py

import { EventMessageTypeNames } from 'n8n-workflow';
import type { JsonObject, JsonValue } from 'n8n-workflow';

import type { EventNamesAuditType } from '.';
import { AbstractEventMessage, isEventMessageOptionsWithType } from './abstract-event-message';
import type { AbstractEventMessageOptions } from './abstract-event-message-options';
import type { AbstractEventPayload } from './abstract-event-payload';

// --------------------------------------
// EventMessage class for Audit events
// --------------------------------------
export interface EventPayloadAudit extends AbstractEventPayload {
	msg?: JsonValue;
	userId?: string;
	userEmail?: string;
	firstName?: string;
	lastName?: string;
	credentialName?: string;
	credentialType?: string;
	credentialId?: string;
	workflowId?: string;
	workflowName?: string;
	activeVersionId?: string | null;
	settingsChanged?: Record<string, { from: JsonValue; to: JsonValue }>;
	variableId?: string;
	variableKey?: string;
}

export interface EventMessageAuditOptions extends AbstractEventMessageOptions {
	eventName: EventNamesAuditType;

	payload?: EventPayloadAudit;
}

export class EventMessageAudit extends AbstractEventMessage {
	readonly __type = EventMessageTypeNames.audit;

	eventName: EventNamesAuditType;

	payload: EventPayloadAudit;

	constructor(options: EventMessageAuditOptions) {
		super(options);
		if (options.payload) this.setPayload(options.payload);
		if (options.anonymize) {
			this.anonymize();
		}
	}

	setPayload(payload: EventPayloadAudit): this {
		this.payload = payload;
		return this;
	}

	deserialize(data: JsonObject): this {
		if (isEventMessageOptionsWithType(data, this.__type)) {
			this.setOptionsOrDefault(data);
			if (data.payload) this.setPayload(data.payload as EventPayloadAudit);
		}
		return this;
	}
}
