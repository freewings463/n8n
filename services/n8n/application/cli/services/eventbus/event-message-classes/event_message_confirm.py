"""
MIGRATION-META:
  source_path: packages/cli/src/eventbus/event-message-classes/event-message-confirm.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/eventbus/event-message-classes 的模块。导入/依赖:外部:luxon；内部:n8n-workflow；本地:无。导出:EventMessageConfirmSource、EventMessageConfirm、isEventMessageConfirm。关键函数/方法:serialize、isEventMessageConfirm。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/eventbus/event-message-classes/event-message-confirm.ts -> services/n8n/application/cli/services/eventbus/event-message-classes/event_message_confirm.py

import { DateTime } from 'luxon';
import type { JsonObject, JsonValue } from 'n8n-workflow';
import { EventMessageTypeNames } from 'n8n-workflow';

export interface EventMessageConfirmSource extends JsonObject {
	id: string;
	name: string;
}

export class EventMessageConfirm {
	readonly __type = EventMessageTypeNames.confirm;

	readonly confirm: string;

	readonly source?: EventMessageConfirmSource;

	readonly ts: DateTime;

	constructor(confirm: string, source?: EventMessageConfirmSource) {
		this.confirm = confirm;
		this.ts = DateTime.now();
		if (source) this.source = source;
	}

	serialize(): JsonValue {
		// TODO: filter payload for sensitive info here?
		return {
			__type: this.__type,
			confirm: this.confirm,
			ts: this.ts.toISO(),
			source: this.source ?? { name: '', id: '' },
		};
	}
}

export const isEventMessageConfirm = (candidate: unknown): candidate is EventMessageConfirm => {
	const o = candidate as EventMessageConfirm;
	if (!o) return false;
	return o.confirm !== undefined && o.ts !== undefined;
};
