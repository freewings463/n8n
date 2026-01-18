"""
MIGRATION-META:
  source_path: packages/cli/src/modules/chat-hub/chat-hub.types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/chat-hub 的类型。导入/依赖:外部:zod；内部:n8n-workflow；本地:无。导出:ModelWithCredentials、BaseMessagePayload、HumanMessagePayload、RegenerateMessagePayload、EditMessagePayload、ContentBlock、MessageRole、MessageRecord 等4项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/chat-hub/chat-hub.types.ts -> services/n8n/application/cli/services/modules/chat-hub/chat_hub_types.py

import type {
	ChatHubConversationModel,
	ChatHubProvider,
	ChatMessageId,
	ChatSessionId,
	ChatAttachment,
} from '@n8n/api-types';
import type { INode, INodeCredentials, IRunExecutionData, IWorkflowBase } from 'n8n-workflow';
import { IconOrEmojiSchema } from 'n8n-workflow';
import { z } from 'zod';

export interface ModelWithCredentials {
	provider: ChatHubProvider;
	model?: string;
	workflowId?: string;
	credentialId: string | null;
	agentId?: string;
	name?: string;
}

export interface BaseMessagePayload {
	userId: string;
	sessionId: ChatSessionId;
	model: ChatHubConversationModel;
	credentials: INodeCredentials;
	timeZone?: string;
}

export interface HumanMessagePayload extends BaseMessagePayload {
	messageId: ChatMessageId;
	message: string;
	previousMessageId: ChatMessageId | null;
	attachments: ChatAttachment[];
	tools: INode[];
	agentName?: string;
}
export interface RegenerateMessagePayload extends BaseMessagePayload {
	retryId: ChatMessageId;
}

export interface EditMessagePayload extends BaseMessagePayload {
	editId: ChatMessageId;
	messageId: ChatMessageId;
	message: string;
	newAttachments: ChatAttachment[];
	keepAttachmentIndices: number[];
}

// From @langchain/core
export type ContentBlock =
	| { type: 'text'; text: string }
	| { type: 'image_url'; image_url: string };

// From packages/@n8n/nodes-langchain/nodes/memory/MemoryManager/MemoryManager.node.ts
export type MessageRole = 'ai' | 'system' | 'user';
export interface MessageRecord {
	type: MessageRole;
	message: string | ContentBlock[];
	hideFromUI: boolean;
}

const ChatTriggerResponseModeSchema = z.enum([
	'streaming',
	'lastNode',
	'responseNode',
	'responseNodes',
]);
export type ChatTriggerResponseMode = z.infer<typeof ChatTriggerResponseModeSchema>;
export type NonStreamingResponseMode = Exclude<
	ChatTriggerResponseMode,
	'streaming' | 'responseNode'
>;

export const chatTriggerParamsShape = z.object({
	availableInChat: z.boolean().optional().default(false),
	agentName: z.string().min(1).optional(),
	agentDescription: z.string().min(1).optional(),
	agentIcon: IconOrEmojiSchema.optional(),
	options: z
		.object({
			allowFileUploads: z.boolean().optional(),
			allowedFilesMimeTypes: z.string().optional(),
			responseMode: ChatTriggerResponseModeSchema.optional(),
		})
		.optional(),
});

export type PreparedChatWorkflow = {
	workflowData: IWorkflowBase;
	executionData: IRunExecutionData;
	responseMode: ChatTriggerResponseMode;
};
