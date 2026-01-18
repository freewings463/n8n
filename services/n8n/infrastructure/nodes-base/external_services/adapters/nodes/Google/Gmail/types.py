"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Gmail/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Gmail 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:Message、ListMessage、MessageListResponse、Label、GmailWorkflowStaticData、GmailWorkflowStaticDataDictionary、GmailTriggerOptions、GmailTriggerFilters 等3项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Gmail/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Gmail/types.py

export type Message = {
	id: string;
	threadId: string;
	labelIds: string[];
	snippet: string;
	historyId: string;
	date?: string;
	headers?: Record<string, string>;
	internalDate?: string;
	sizeEstimate: number;
	raw: string;
	payload: MessagePart;
};

export type ListMessage = Pick<Message, 'id' | 'threadId'>;

export type MessageListResponse = {
	messages?: ListMessage[];
	nextPageToken?: string;
	resultSizeEstimate: number;
};

type GmailHeader = {
	name: string;
	value: string;
};

type MessagePart = {
	partId: string;
	mimeType: string;
	filename: string;
	headers: GmailHeader[];
	body: MessagePartBody;
	parts: MessagePart[];
};

type MessagePartBody = {
	attachmentId: string;
	size: number;
	data: string;
};

export type Label = {
	id: string;
	name: string;
	messageListVisibility?: 'hide';
	labelListVisibility?: 'labelHide';
	type?: 'system';
};

export type GmailWorkflowStaticData = {
	lastTimeChecked?: number;
	possibleDuplicates?: string[];
};
export type GmailWorkflowStaticDataDictionary = Record<string, GmailWorkflowStaticData>;

export type GmailTriggerOptions = Partial<{
	dataPropertyAttachmentsPrefixName: string;
	downloadAttachments: boolean;
}>;

export type GmailTriggerFilters = Partial<{
	sender: string;
	q: string;
	includeSpamTrash: boolean;
	includeDrafts: boolean;
	readStatus: 'read' | 'unread' | 'both';
	labelIds: string[];
	receivedAfter: number;
}>;

export type GmailMessage = {
	id: string;
	threadId: string;
	labelIds: string[];
	snippet: string;
	historyId: string;
	internalDate?: string;
	headers?: Record<string, string>;
	sizeEstimate: number;
	raw: string;
	payload: MessagePart;
};

export type GmailMessageMetadata = Pick<GmailMessage, 'id' | 'threadId' | 'labelIds' | 'payload'>;

export type GmailUserProfile = {
	emailAddress: string;
	messagesTotal: number;
	threadsTotal: number;
	historyId: string;
};
