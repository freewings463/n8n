"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Chat/MessageInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Chat 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IMessage、IMessageUi、IUser、Type。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Chat/MessageInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Chat/MessageInterface.py

import type { IDataObject } from 'n8n-workflow';

export interface IMessage {
	name?: string;
	sender?: IUser;
	createTime?: string;
	text?: string;
	cards?: IDataObject[];
	previewText?: string;
	annotations?: IDataObject[];
	thread?: IDataObject[];
	space?: IDataObject;
	fallbackText?: string;
	actionResponse?: IDataObject;
	argumentText?: string;
	slashCommand?: IDataObject;
	attachment?: IDataObject[];
}

export interface IMessageUi {
	text?: string;
	cards?: {
		metadata: IDataObject[];
	};
}

export interface IUser {
	name?: string;
	displayName?: string;
	domainId?: string;
	type?: Type;
	isAnonymous?: boolean;
}
const Types = {
	TYPE_UNSPECIFIED: 0,
	HUMAN: 1,
	BOT: 2,
} as const;

export type Type = (typeof Types)[keyof typeof Types];

// // TODO: define other interfaces
//
// export interface IMessage {s
// 	name?: string;
// 	sender?: IUser;
// 	createTime?: string;
// 	text?: string;
// 	cards?: ICard[];
// 	previewText?: string;
// 	annotations?: IAnnotation[];
// 	thread?: IThread[];
// 	space?: ISpace;
// 	fallbackText?: string;
// 	actionResponse?: IActionResponse;
// 	argumentText?: string;
// 	slashCommand?: ISlashCommand;
// 	attachment?: IAttachment[];
// }
//
// export interface ICard {
// 	header?: ICardHeader;
// 	sections?: ISection[];
// 	cardActions?: ICardAction[];
// 	name?: string;
// }
//
// export interface ICardHeader {
// 	title: string;
// 	subtitle: string;
// 	imageStyle: ImageStyleType;
// 	imageUrl: string;
// }
// enum ImageStyleType {
// 	'IMAGE_STYLE_UNSPECIFIED',
// 	'IMAGE',
// 	'AVATAR',
// }
//
// export interface ISection {
//
// }
//
// export interface ICardAction {
//
// }
//
// export interface IAnnotation {
//
// }
//
// export interface IThread {
//
// }
//
// export interface ISpace {
//
// }
//
// export interface IActionResponse {
//
// }
//
// export interface ISlashCommand {
//
// }
//
// export interface IAttachment {
// // attachments are not available for bots
// }
