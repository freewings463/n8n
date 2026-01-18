"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/v2/descriptions/rlc.description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:calendarRLC、contactRLC、draftRLC、messageRLC、eventRLC、folderRLC、attachmentRLC。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/v2/descriptions/rlc.description.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/v2/descriptions/rlc_description.py

import type { INodeProperties } from 'n8n-workflow';

export const calendarRLC: INodeProperties = {
	displayName: 'Calendar',
	name: 'calendarId',
	type: 'resourceLocator',
	default: { mode: 'list', value: '' },
	required: true,
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			placeholder: 'Select a calendar...',
			typeOptions: {
				searchListMethod: 'searchCalendars',
				searchable: true,
			},
		},
		{
			displayName: 'ID',
			name: 'id',
			type: 'string',
			placeholder: 'e.g. AAAkAAAhAAA0BBc5LLLwOOOtNNNkZS05Nz...',
		},
	],
};

export const contactRLC: INodeProperties = {
	displayName: 'Contact',
	name: 'contactId',
	type: 'resourceLocator',
	default: { mode: 'list', value: '' },
	required: true,
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			placeholder: 'Select a contact...',
			typeOptions: {
				searchListMethod: 'searchContacts',
				searchable: true,
			},
		},
		{
			displayName: 'ID',
			name: 'id',
			type: 'string',
			placeholder: 'e.g. AAAkAAAhAAA0BBc5LLLwOOOtNNNkZS05Nz...',
		},
	],
};

export const draftRLC: INodeProperties = {
	displayName: 'Draft',
	name: 'draftId',
	type: 'resourceLocator',
	default: { mode: 'list', value: '' },
	required: true,
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			placeholder: 'Select a draft...',
			typeOptions: {
				searchListMethod: 'searchDrafts',
				searchable: true,
			},
		},
		{
			displayName: 'ID',
			name: 'id',
			type: 'string',
			placeholder: 'e.g. AAAkAAAhAAA0BBc5LLLwOOOtNNNkZS05Nz...',
		},
	],
};

export const messageRLC: INodeProperties = {
	displayName: 'Message',
	name: 'messageId',
	type: 'resourceLocator',
	default: { mode: 'list', value: '' },
	required: true,
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			placeholder: 'Select a message...',
			typeOptions: {
				searchListMethod: 'searchMessages',
				searchable: true,
			},
		},
		{
			displayName: 'ID',
			name: 'id',
			type: 'string',
			placeholder: 'e.g. AAAkAAAhAAA0BBc5LLLwOOOtNNNkZS05Nz...',
		},
	],
};

export const eventRLC: INodeProperties = {
	displayName: 'Event',
	name: 'eventId',
	type: 'resourceLocator',
	default: { mode: 'list', value: '' },
	required: true,
	typeOptions: {
		loadOptionsDependsOn: ['calendarId.value'],
	},
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			placeholder: 'Select a event...',
			typeOptions: {
				searchListMethod: 'searchEvents',
				searchable: true,
			},
		},
		{
			displayName: 'Link',
			name: 'url',
			type: 'string',
			placeholder: 'e.g. https://outlook.office365.com/calendar/item/AAMkADlhOTA0M...UAAA%3D',
			extractValue: {
				type: 'regex',
				regex:
					'https:\\/\\/outlook\\.office365\\.com\\/calendar\\/item\\/([A-Za-z0-9%]+)(?:\\/.*|)',
			},
			validation: [
				{
					type: 'regex',
					properties: {
						regex:
							'https:\\/\\/outlook\\.office365\\.com\\/calendar\\/item\\/([A-Za-z0-9%]+)(?:\\/.*|)',
						errorMessage: 'Not a valid Outlook Event URL',
					},
				},
			],
		},
		{
			displayName: 'ID',
			name: 'id',
			type: 'string',
			placeholder: 'e.g. AAAkAAAhAAA0BBc5LLLwOOOtNNNkZS05Nz...',
		},
	],
};

export const folderRLC: INodeProperties = {
	displayName: 'Folder',
	name: 'folderId',
	type: 'resourceLocator',
	default: { mode: 'list', value: '' },
	required: true,
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			placeholder: 'Select a folder...',
			typeOptions: {
				searchListMethod: 'searchFolders',
				searchable: true,
			},
		},
		{
			displayName: 'Link',
			name: 'url',
			type: 'string',
			placeholder: 'e.g. https://outlook.office365.com/mail/AAMkADlhOT...AAA%3D',
			extractValue: {
				type: 'regex',
				regex: 'https:\\/\\/outlook\\.office365\\.com\\/mail\\/([A-Za-z0-9%]+)(?:\\/.*|)',
			},
			validation: [
				{
					type: 'regex',
					properties: {
						regex: 'https:\\/\\/outlook\\.office365\\.com\\/mail\\/([A-Za-z0-9%]+)(?:\\/.*|)',
						errorMessage: 'Not a valid Outlook Folder URL',
					},
				},
			],
		},
		{
			displayName: 'ID',
			name: 'id',
			type: 'string',
			placeholder: 'e.g. AAAkAAAhAAA0BBc5LLLwOOOtNNNkZS05Nz...',
		},
	],
};

export const attachmentRLC: INodeProperties = {
	displayName: 'Attachment',
	name: 'attachmentId',
	type: 'resourceLocator',
	default: { mode: 'list', value: '' },
	required: true,
	typeOptions: {
		loadOptionsDependsOn: ['messageId.value'],
	},
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			placeholder: 'Select a attachment...',
			typeOptions: {
				searchListMethod: 'searchAttachments',
				searchable: false,
			},
		},
		{
			displayName: 'ID',
			name: 'id',
			type: 'string',
			placeholder: 'e.g. AAAkAAAhAAA0BBc5LLLwOOOtNNNkZS05Nz...',
		},
	],
};
