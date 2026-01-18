"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Clockify/ProjectInterfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Clockify 的节点。导入/依赖:外部:无；内部:无；本地:./CommonDtos。导出:IProjectDto、IProjectRequest、ITaskDto。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Clockify/ProjectInterfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Clockify/ProjectInterfaces.py

import type { IHourlyRateDto, IMembershipDto } from './CommonDtos';

const Estimates = {
	AUTO: 'AUTO',
	MANUAL: 'MANUAL',
} as const;

type EstimateEnum = (typeof Estimates)[keyof typeof Estimates];

interface IEstimateDto {
	estimate: string;
	type: EstimateEnum;
}

export interface IProjectDto {
	archived: boolean;
	billable: boolean;
	clientId: string;
	clientName: string | undefined;
	color: string;
	duration: string | undefined;
	estimate: IEstimateDto | undefined;
	hourlyRate: IHourlyRateDto | undefined;
	id: string;
	memberships: IMembershipDto[] | undefined;
	name: string;
	isPublic: boolean;
	workspaceId: string;
	note: string | undefined;
}

export interface IProjectRequest {
	name: string;
	clientId: string;
	isPublic: boolean;
	estimate: IEstimateDto;
	color: string;
	note: string;
	billable: boolean;
	hourlyRate: IHourlyRateDto;
	memberships: IMembershipDto;
	tasks: ITaskDto;
}

const TaskStatuses = {
	ACTIVE: 'ACTIVE',
	DONE: 'DONE',
} as const;

type TaskStatusEnum = (typeof TaskStatuses)[keyof typeof TaskStatuses];

export interface ITaskDto {
	assigneeIds: object;
	estimate: string;
	id: string;
	name: string;
	projectId: string;
	status: TaskStatusEnum;
	'is-active': boolean;
}
