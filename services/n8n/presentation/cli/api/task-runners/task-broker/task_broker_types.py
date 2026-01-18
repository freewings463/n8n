"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/task-broker/task-broker-types.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/task-runners/task-broker 的类型。导入/依赖:外部:express、ws；内部:@n8n/task-runner；本地:../../requests。导出:DisconnectAnalyzer、TaskBrokerServerInitRequest、TaskBrokerServerInitResponse、DisconnectReason、DisconnectErrorOptions。关键函数/方法:toDisconnectError。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/task-broker/task-broker-types.ts -> services/n8n/presentation/cli/api/task-runners/task-broker/task_broker_types.py

import type { TaskRunner } from '@n8n/task-runner';
import type { Response } from 'express';
import type WebSocket from 'ws';

import type { AuthlessRequest } from '../../requests';

export interface DisconnectAnalyzer {
	isCloudDeployment: boolean;

	toDisconnectError(opts: DisconnectErrorOptions): Promise<Error>;
}

export interface TaskBrokerServerInitRequest
	extends AuthlessRequest<{}, {}, {}, { id: TaskRunner['id']; token?: string }> {
	ws: WebSocket;
}

export type TaskBrokerServerInitResponse = Response & { req: TaskBrokerServerInitRequest };

export type DisconnectReason = 'shutting-down' | 'failed-heartbeat-check' | 'unknown';

export type DisconnectErrorOptions = {
	runnerId?: TaskRunner['id'];
	reason?: DisconnectReason;
	heartbeatInterval?: number;
};
