"""
MIGRATION-META:
  source_path: packages/workflow/src/cron.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src 的工作流模块。导入/依赖:外部:无；内部:无；本地:./interfaces、./utils。导出:TriggerTime、toCronExpression。关键函数/方法:toCronExpression。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/cron.ts -> services/n8n/domain/workflow/services/cron.py

import type { CronExpression } from './interfaces';
import { randomInt } from './utils';

interface BaseTriggerTime<T extends string> {
	mode: T;
}

interface CustomTrigger extends BaseTriggerTime<'custom'> {
	cronExpression: CronExpression;
}

interface EveryX<U extends string> extends BaseTriggerTime<'everyX'> {
	unit: U;
	value: number;
}

type EveryMinute = BaseTriggerTime<'everyMinute'>;
type EveryXMinutes = EveryX<'minutes'>;

interface EveryHour extends BaseTriggerTime<'everyHour'> {
	minute: number; // 0 - 59
}
type EveryXHours = EveryX<'hours'>;

interface EveryDay extends BaseTriggerTime<'everyDay'> {
	hour: number; // 0 - 23
	minute: number; // 0 - 59
}

interface EveryWeek extends BaseTriggerTime<'everyWeek'> {
	hour: number; // 0 - 23
	minute: number; // 0 - 59
	weekday: number; // 0 - 6(Sun - Sat)
}

interface EveryMonth extends BaseTriggerTime<'everyMonth'> {
	hour: number; // 0 - 23
	minute: number; // 0 - 59
	dayOfMonth: number; // 1 - 31
}

export type TriggerTime =
	| CustomTrigger
	| EveryMinute
	| EveryXMinutes
	| EveryHour
	| EveryXHours
	| EveryDay
	| EveryWeek
	| EveryMonth;

export const toCronExpression = (item: TriggerTime): CronExpression => {
	const randomSecond = randomInt(60);

	if (item.mode === 'everyMinute') return `${randomSecond} * * * * *`;
	if (item.mode === 'everyHour') return `${randomSecond} ${item.minute} * * * *`;

	if (item.mode === 'everyX') {
		if (item.unit === 'minutes') return `${randomSecond} */${item.value} * * * *`;

		const randomMinute = randomInt(60);
		if (item.unit === 'hours') return `${randomSecond} ${randomMinute} */${item.value} * * *`;
	}
	if (item.mode === 'everyDay') return `${randomSecond} ${item.minute} ${item.hour} * * *`;
	if (item.mode === 'everyWeek')
		return `${randomSecond} ${item.minute} ${item.hour} * * ${item.weekday}`;

	if (item.mode === 'everyMonth')
		return `${randomSecond} ${item.minute} ${item.hour} ${item.dayOfMonth} * *`;

	return item.cronExpression.trim() as CronExpression;
};
