"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Schedule/SchedulerInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Schedule 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:IRecurrenceRule、ScheduleInterval、Rule。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Schedule/SchedulerInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Schedule/SchedulerInterface.py

import type { CronExpression } from 'n8n-workflow';

export type IRecurrenceRule =
	| { activated: false }
	| {
			activated: true;
			index: number;
			intervalSize: number;
			typeInterval: 'hours' | 'days' | 'weeks' | 'months';
	  };

export type ScheduleInterval =
	| {
			field: 'cronExpression';
			expression: CronExpression;
	  }
	| {
			field: 'seconds';
			secondsInterval: number;
	  }
	| {
			field: 'minutes';
			minutesInterval: number;
	  }
	| {
			field: 'hours';
			hoursInterval: number;
			triggerAtMinute?: number;
	  }
	| {
			field: 'days';
			daysInterval: number;
			triggerAtHour?: number;
			triggerAtMinute?: number;
	  }
	| {
			field: 'weeks';
			weeksInterval: number;
			triggerAtDay: number[];
			triggerAtHour?: number;
			triggerAtMinute?: number;
	  }
	| {
			field: 'months';
			monthsInterval: number;
			triggerAtDayOfMonth?: number;
			triggerAtHour?: number;
			triggerAtMinute?: number;
	  };

export interface Rule {
	interval: ScheduleInterval[];
}
