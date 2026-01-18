"""
MIGRATION-META:
  source_path: packages/cli/src/chat/chat-service.types.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/chat 的服务。导入/依赖:外部:ws、zod；内部:无；本地:无。导出:ChatRequest、Session、chatMessageSchema、ChatMessage。关键函数/方法:无。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected WebSocket adapter/types (ws)
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/chat/chat-service.types.ts -> services/n8n/presentation/cli/api/ws/chat/chat_service_types.py

import type { IncomingMessage } from 'http';
import type { WebSocket } from 'ws';
import { z } from 'zod';

export interface ChatRequest extends IncomingMessage {
	url: string;
	query: {
		sessionId: string;
		executionId: string;
		isPublic?: boolean;
	};
	ws: WebSocket;
}

export type Session = {
	connection: WebSocket;
	executionId: string;
	sessionId: string;
	intervalId: NodeJS.Timeout;
	nodeWaitingForChatResponse?: string;
	isPublic: boolean;
	isProcessing: boolean;
	lastHeartbeat?: number;
};

export const chatMessageSchema = z.object({
	sessionId: z.string(),
	action: z.literal('sendMessage'),
	chatInput: z.string(),
	files: z
		.array(
			z.object({
				name: z.string(),
				type: z.string(),
				data: z.string(),
			}),
		)
		.optional(),
});

export type ChatMessage = z.infer<typeof chatMessageSchema>;
