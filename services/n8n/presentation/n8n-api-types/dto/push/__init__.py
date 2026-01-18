"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/push/index.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/push 的入口。导入/依赖:外部:无；内部:无；本地:./builder-credits、./collaboration、./debug、./execution 等4项。导出:PushMessage、PushType、PushPayload。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/push/index.ts -> services/n8n/presentation/n8n-api-types/dto/push/__init__.py

import type { BuilderCreditsPushMessage } from './builder-credits';
import type { CollaborationPushMessage } from './collaboration';
import type { DebugPushMessage } from './debug';
import type { ExecutionPushMessage } from './execution';
import type { HotReloadPushMessage } from './hot-reload';
import type { WebhookPushMessage } from './webhook';
import type { WorkerPushMessage } from './worker';
import type { WorkflowPushMessage } from './workflow';

export type PushMessage =
	| ExecutionPushMessage
	| WorkflowPushMessage
	| HotReloadPushMessage
	| WebhookPushMessage
	| WorkerPushMessage
	| CollaborationPushMessage
	| DebugPushMessage
	| BuilderCreditsPushMessage;

export type PushType = PushMessage['type'];

export type PushPayload<T extends PushType> = Extract<PushMessage, { type: T }>['data'];
