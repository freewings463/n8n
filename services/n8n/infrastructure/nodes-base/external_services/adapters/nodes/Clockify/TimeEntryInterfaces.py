"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Clockify/TimeEntryInterfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Clockify 的节点。导入/依赖:外部:无；内部:无；本地:./CommonDtos。导出:ITimeEntryRequest、ITimeEntryDto。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Clockify/TimeEntryInterfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Clockify/TimeEntryInterfaces.py

import type { ITimeIntervalDto } from './CommonDtos';

interface ITimeEntriesDurationRequest {
	start: string;
	end: string;
}

export interface ITimeEntryRequest {
	id: string;
	start: string;
	billable: boolean;
	description: string;
	projectId: string;
	userId: string;
	taskId?: string | null;
	end: string;
	tagIds?: string[] | undefined;
	timeInterval: ITimeEntriesDurationRequest;
	workspaceId: string;
	isLocked: boolean;
}

export interface ITimeEntryDto {
	billable: boolean;
	description: string;
	id: string;
	isLocked: boolean;
	projectId: string;
	tagIds: string[];
	taskId: string;
	timeInterval: ITimeIntervalDto;
	userId: string;
	workspaceId: string;
}
