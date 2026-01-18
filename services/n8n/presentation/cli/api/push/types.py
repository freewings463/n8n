"""
MIGRATION-META:
  source_path: packages/cli/src/push/types.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/push 的类型。导入/依赖:外部:express、ws；内部:@n8n/db；本地:无。导出:PushRequest、SSEPushRequest、WebSocketPushRequest、PushResponse、OnPushMessage。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/push/types.ts -> services/n8n/presentation/cli/api/push/types.py

import type { AuthenticatedRequest, User } from '@n8n/db';
import type { Request, Response } from 'express';
import type { WebSocket } from 'ws';

// TODO: move all push related types here

export type PushRequest = AuthenticatedRequest<{}, {}, {}, { pushRef: string }>;

export type SSEPushRequest = PushRequest & { ws: undefined };
export type WebSocketPushRequest = PushRequest & {
	ws: WebSocket;
	headers: Request['headers'];
};

export type PushResponse = Response & {
	req: PushRequest;
	/**
	 * `flush()` is defined in the compression middleware.
	 * This is necessary because the compression middleware sometimes waits
	 * for a certain amount of data before sending the data to the client
	 */
	flush: () => void;
};

export interface OnPushMessage {
	pushRef: string;
	userId: User['id'];
	msg: unknown;
}
