"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Calendar/EventInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Calendar 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IReminder、IConferenceData、IEvent、RecurringEventInstance。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Calendar/EventInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Calendar/EventInterface.py

import type { IDataObject } from 'n8n-workflow';

export interface IReminder {
	useDefault?: boolean;
	overrides?: IDataObject[];
}

export interface IConferenceData {
	createRequest?: {
		requestId: string;
		conferenceSolution: {
			type: string;
		};
	};
}

export interface IEvent {
	attendees?: IDataObject[];
	colorId?: string;
	description?: string;
	end?: IDataObject;
	guestsCanInviteOthers?: boolean;
	guestsCanModify?: boolean;
	guestsCanSeeOtherGuests?: boolean;
	id?: string;
	location?: string;
	maxAttendees?: number;
	recurrence?: string[];
	reminders?: IReminder;
	sendUpdates?: string;
	start?: IDataObject;
	summary?: string;
	transparency?: string;
	visibility?: string;
	conferenceData?: IConferenceData;
}

export type RecurringEventInstance = {
	recurringEventId?: string;
	start: { dateTime: string; date: string };
};
