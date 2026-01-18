"""
MIGRATION-META:
  source_path: packages/cli/src/modules/insights/database/entities/insights-raw.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/insights/database 的Insights模块。导入/依赖:外部:无；内部:@n8n/config、@n8n/db、@n8n/di、@n8n/typeorm、n8n-workflow；本地:./insights-shared。导出:InsightsRaw。关键函数/方法:无。用于承载Insights实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected TypeORM @Entity model
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/insights/database/entities/insights-raw.ts -> services/n8n/infrastructure/cli/persistence/models/insights_raw.py

import { GlobalConfig } from '@n8n/config';
import { DateTimeColumn } from '@n8n/db';
import { Container } from '@n8n/di';
import { BaseEntity, Column, Entity, PrimaryGeneratedColumn } from '@n8n/typeorm';
import { UnexpectedError } from 'n8n-workflow';

import { isValidTypeNumber, NumberToType, TypeToNumber } from './insights-shared';

export const { type: dbType } = Container.get(GlobalConfig).database;

@Entity()
export class InsightsRaw extends BaseEntity {
	constructor() {
		super();
		this.timestamp = new Date();
	}

	@PrimaryGeneratedColumn()
	id: number;

	@Column()
	metaId: number;

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

	@DateTimeColumn({ name: 'timestamp' })
	timestamp: Date;
}
