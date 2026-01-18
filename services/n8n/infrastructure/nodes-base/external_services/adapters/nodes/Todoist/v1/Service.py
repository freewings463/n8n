"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Todoist/v1/Service.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Todoist/v1 的服务。导入/依赖:外部:无；内部:n8n-workflow；本地:../GenericFunctions。导出:TodoistService、OperationType、Section、Service、TodoistResponse。关键函数/方法:execute。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Todoist/v1/Service.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Todoist/v1/Service.py

import type { IDataObject } from 'n8n-workflow';

import {
	CloseHandler,
	CreateHandler,
	DeleteHandler,
	GetAllHandler,
	GetHandler,
	MoveHandler,
	ReopenHandler,
	SyncHandler,
	UpdateHandler,
} from './OperationHandler';
import type { Context } from '../GenericFunctions';

export class TodoistService implements Service {
	async execute(
		ctx: Context,
		operation: OperationType,
		itemIndex: number,
	): Promise<TodoistResponse> {
		return await this.handlers[operation].handleOperation(ctx, itemIndex);
	}

	private handlers = {
		create: new CreateHandler(),
		close: new CloseHandler(),
		delete: new DeleteHandler(),
		get: new GetHandler(),
		getAll: new GetAllHandler(),
		reopen: new ReopenHandler(),
		update: new UpdateHandler(),
		move: new MoveHandler(),
		sync: new SyncHandler(),
	};
}

export type OperationType =
	| 'create'
	| 'close'
	| 'delete'
	| 'get'
	| 'getAll'
	| 'reopen'
	| 'update'
	| 'move'
	| 'sync';

export interface Section {
	name: string;
	id: string;
}

export interface Service {
	execute(ctx: Context, operation: OperationType, itemIndex: number): Promise<TodoistResponse>;
}

export interface TodoistResponse {
	success?: boolean;
	data?: IDataObject;
}
