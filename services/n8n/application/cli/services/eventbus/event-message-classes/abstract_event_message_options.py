"""
MIGRATION-META:
  source_path: packages/cli/src/eventbus/event-message-classes/abstract-event-message-options.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/eventbus/event-message-classes 的模块。导入/依赖:外部:luxon；内部:n8n-workflow；本地:.、./abstract-event-payload。导出:AbstractEventMessageOptions。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/eventbus/event-message-classes/abstract-event-message-options.ts -> services/n8n/application/cli/services/eventbus/event-message-classes/abstract_event_message_options.py

import type { DateTime } from 'luxon';
import type { EventMessageTypeNames } from 'n8n-workflow';

import type { EventNamesTypes } from '.';
import type { AbstractEventPayload } from './abstract-event-payload';

export interface AbstractEventMessageOptions {
	__type?: EventMessageTypeNames;
	id?: string;
	ts?: DateTime | string;
	eventName: EventNamesTypes;
	message?: string;
	payload?: AbstractEventPayload;
	anonymize?: boolean;
}
