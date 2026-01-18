"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Clockify/CommonDtos.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Clockify 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:IHourlyRateDto、IMembershipDto、ITagDto、ITaskDto、ITimeIntervalDto。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Clockify/CommonDtos.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Clockify/CommonDtos.py

export interface IHourlyRateDto {
	amount: number;
	currency: string;
}

const MembershipStatuses = {
	PENDING: 'PENDING',
	ACTIVE: 'ACTIVE',
	DECLINED: 'DECLINED',
	INACTIVE: 'INACTIVE',
} as const;

type MembershipStatusEnum = (typeof MembershipStatuses)[keyof typeof MembershipStatuses];

const TaskStatuses = {
	ACTIVE: 'ACTIVE',
	DONE: 'DONE',
} as const;

type TaskStatusEnum = (typeof TaskStatuses)[keyof typeof TaskStatuses];

export interface IMembershipDto {
	hourlyRate: IHourlyRateDto;
	membershipStatus: MembershipStatusEnum;
	membershipType: string;
	targetId: string;
	userId: string;
}

export interface ITagDto {
	id: string;
	name: any;
	workspaceId: string;
	archived: boolean;
}

export interface ITaskDto {
	assigneeIds: object;
	estimate: string;
	id: string;
	name: any;
	workspaceId: string;
	projectId: string;
	'is-active': boolean;
	status: TaskStatusEnum;
}

export interface ITimeIntervalDto {
	duration: string;
	end: string;
	start: string;
}
