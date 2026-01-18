"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Clockify/WorkpaceInterfaces.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Clockify 的节点。导入/依赖:外部:无；内部:无；本地:./CommonDtos。导出:AdminOnlyPages、AdminOnlyPagesEnum、DaysOfWeek、DaysOfWeekEnum、DatePeriods、DatePeriodEnum、AutomaticLockTypes、AutomaticLockTypeEnum 等2项。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Clockify/WorkpaceInterfaces.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Clockify/WorkpaceInterfaces.py

import type { IHourlyRateDto, IMembershipDto } from './CommonDtos';

export const AdminOnlyPages = {
	PROJECT: 'PROJECT',
	TEAM: 'TEAM',
	REPORTS: 'REPORTS',
} as const;

export type AdminOnlyPagesEnum = (typeof AdminOnlyPages)[keyof typeof AdminOnlyPages];

export const DaysOfWeek = {
	MONDAY: 'MONDAY',
	TUESDAY: 'TUESDAY',
	WEDNESDAY: 'WEDNESDAY',
	THURSDAY: 'THURSDAY',
	FRIDAY: 'FRIDAY',
	SATURDAY: 'SATURDAY',
	SUNDAY: 'SUNDAY',
} as const;

export type DaysOfWeekEnum = (typeof DaysOfWeek)[keyof typeof DaysOfWeek];

export const DatePeriods = {
	DAYS: 'DAYS',
	WEEKS: 'WEEKS',
	MONTHS: 'MONTHS',
} as const;

export type DatePeriodEnum = (typeof DatePeriods)[keyof typeof DatePeriods];

export const AutomaticLockTypes = {
	WEEKLY: 'WEEKLY',
	MONTHLY: 'MONTHLY',
	OLDER_THAN: 'OLDER_THAN',
} as const;

export type AutomaticLockTypeEnum = (typeof AutomaticLockTypes)[keyof typeof AutomaticLockTypes];

interface IAutomaticLockDto {
	changeDay: DaysOfWeekEnum;
	dayOfMonth: number;
	firstDay: DaysOfWeekEnum;
	olderThanPeriod: DatePeriodEnum;
	olderThanValue: number;
	type: AutomaticLockTypeEnum;
}

interface IRound {
	minutes: string;
	round: string;
}

interface IWorkspaceSettingsDto {
	adminOnlyPages: AdminOnlyPagesEnum[];
	automaticLock: IAutomaticLockDto;
	canSeeTimeSheet: boolean;
	defaultBillableProjects: boolean;
	forceDescription: boolean;
	forceProjects: boolean;
	forceTags: boolean;
	forceTasks: boolean;
	lockTimeEntries: string;
	onlyAdminsCreateProject: boolean;
	onlyAdminsCreateTag: boolean;
	onlyAdminsSeeAllTimeEntries: boolean;
	onlyAdminsSeeBillableRates: boolean;
	onlyAdminsSeeDashboard: boolean;
	onlyAdminsSeePublicProjectsEntries: boolean;
	projectFavorites: boolean;
	projectGroupingLabel: string;
	projectPickerSpecialFilter: boolean;
	round: IRound;
	timeRoundingInReports: boolean;
	trackTimeDownToSecond: boolean;
}

export interface IWorkspaceDto {
	hourlyRate: IHourlyRateDto;
	id: string;
	imageUrl: string;
	memberships: IMembershipDto[];
	name: string;
	workspaceSettings: IWorkspaceSettingsDto;
}

export interface IClientDto {
	id: string;
	name: string;
	workspaceId: string;
}
