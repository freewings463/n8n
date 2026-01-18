"""
MIGRATION-META:
  source_path: packages/cli/src/modules/insights/database/entities/insights-by-period.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/insights/database 的Insights模块。导入/依赖:外部:无；内部:@n8n/db、n8n-workflow；本地:./insights-metadata、./insights-shared。导出:InsightsByPeriod。关键函数/方法:无。用于承载Insights实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/insights/database/entities/insights-by-period.ts -> services/n8n/infrastructure/cli/persistence/models/insights_by_period.py

import { DateTimeColumn } from '@n8n/db';
import {
	BaseEntity,
	Column,
	Entity,
	JoinColumn,
	ManyToOne,
	PrimaryGeneratedColumn,
} from '@n8n/typeorm';
import { UnexpectedError } from 'n8n-workflow';

import { InsightsMetadata } from './insights-metadata';
import type { PeriodUnit } from './insights-shared';
import {
	isValidPeriodNumber,
	isValidTypeNumber,
	NumberToPeriodUnit,
	NumberToType,
	PeriodUnitToNumber,
	TypeToNumber,
} from './insights-shared';

@Entity()
export class InsightsByPeriod extends BaseEntity {
	@PrimaryGeneratedColumn()
	id: number;

	@Column()
	metaId: number;

	@ManyToOne(() => InsightsMetadata)
	@JoinColumn({ name: 'metaId' })
	metadata: InsightsMetadata;

	@Column({ name: 'type', type: 'int' })
	private type_: number;

	get type() {
		if (!isValidTypeNumber(this.type_)) {
			throw new UnexpectedError(
				`Type '${this.type_}' is not a valid type for 'InsightsByPeriod.type'`,
			);
		}

		return NumberToType[this.type_];
	}

	set type(value: keyof typeof TypeToNumber) {
		this.type_ = TypeToNumber[value];
	}

	/**
	 * Stored as BIGINT in database (see migration 1759399811000).
	 * JavaScript number type has precision limits at ±2^53-1 (9,007,199,254,740,991).
	 * Values exceeding Number.MAX_SAFE_INTEGER will lose precision.
	 */
	@Column()
	value: number;

	@Column({ name: 'periodUnit' })
	private periodUnit_: number;

	get periodUnit() {
		if (!isValidPeriodNumber(this.periodUnit_)) {
			throw new UnexpectedError(
				`Period unit '${this.periodUnit_}' is not a valid unit for 'InsightsByPeriod.periodUnit'`,
			);
		}

		return NumberToPeriodUnit[this.periodUnit_];
	}

	set periodUnit(value: PeriodUnit) {
		this.periodUnit_ = PeriodUnitToNumber[value];
	}

	@DateTimeColumn()
	periodStart: Date;
}
