"""
MIGRATION-META:
  source_path: packages/cli/src/modules/insights/insights-compaction.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/insights 的Insights服务。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/di 等1项；本地:../repositories/insights-by-period.repository、../repositories/insights-raw.repository、./insights.config。导出:InsightsCompactionService。关键函数/方法:startCompactionTimer、async、stopCompactionTimer、clearInterval、compactInsights、compactRawToHour、compactHourToDay、compactDayToWeek。用于封装Insights业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/insights/insights-compaction.service.ts -> services/n8n/application/cli/services/insights/insights_compaction_service.py

import { Logger } from '@n8n/backend-common';
import { Service } from '@n8n/di';

import { InsightsByPeriodRepository } from './database/repositories/insights-by-period.repository';
import { InsightsRawRepository } from './database/repositories/insights-raw.repository';
import { InsightsConfig } from './insights.config';
import { Time } from '@n8n/constants';

/**
 * This service is responsible for compacting lower granularity insights data
 * into higher granularity to control the size of the insights data.
 */
@Service()
export class InsightsCompactionService {
	private compactInsightsTimer: NodeJS.Timeout | undefined;

	constructor(
		private readonly insightsByPeriodRepository: InsightsByPeriodRepository,
		private readonly insightsRawRepository: InsightsRawRepository,
		private readonly insightsConfig: InsightsConfig,
		private readonly logger: Logger,
	) {
		this.logger = this.logger.scoped('insights');
	}

	startCompactionTimer() {
		this.stopCompactionTimer();
		this.compactInsightsTimer = setInterval(
			async () => await this.compactInsights(),
			this.insightsConfig.compactionIntervalMinutes * Time.minutes.toMilliseconds,
		);
		this.logger.debug('Started compaction timer');
	}

	stopCompactionTimer() {
		if (this.compactInsightsTimer !== undefined) {
			clearInterval(this.compactInsightsTimer);
			this.compactInsightsTimer = undefined;
			this.logger.debug('Stopped compaction timer');
		}
	}

	async compactInsights() {
		let numberOfCompactedRawData: number;

		// Compact raw data to hourly aggregates
		do {
			this.logger.debug('Compacting raw data to hourly aggregates');
			numberOfCompactedRawData = await this.compactRawToHour();
			this.logger.debug(`Compacted ${numberOfCompactedRawData} raw data to hourly aggregates`);
		} while (numberOfCompactedRawData === this.insightsConfig.compactionBatchSize);

		let numberOfCompactedHourData: number;

		// Compact hourly data to daily aggregates
		do {
			this.logger.debug('Compacting hourly data to daily aggregates');
			numberOfCompactedHourData = await this.compactHourToDay();
			this.logger.debug(`Compacted ${numberOfCompactedHourData} hourly data to daily aggregates`);
		} while (numberOfCompactedHourData === this.insightsConfig.compactionBatchSize);

		let numberOfCompactedDayData: number;
		// Compact daily data to weekly aggregates
		do {
			this.logger.debug('Compacting daily data to weekly aggregates');
			numberOfCompactedDayData = await this.compactDayToWeek();
			this.logger.debug(`Compacted ${numberOfCompactedDayData} daily data to weekly aggregates`);
		} while (numberOfCompactedDayData === this.insightsConfig.compactionBatchSize);
	}

	/**
	 * Compacts raw data to hourly aggregates
	 */
	async compactRawToHour() {
		// Build the query to gather raw insights data for the batch
		const batchQuery = this.insightsRawRepository.getRawInsightsBatchQuery(
			this.insightsConfig.compactionBatchSize,
		);

		return await this.insightsByPeriodRepository.compactSourceDataIntoInsightPeriod({
			sourceBatchQuery: batchQuery,
			sourceTableName: this.insightsRawRepository.metadata.tableName,
			periodUnitToCompactInto: 'hour',
		});
	}

	/**
	 * Compacts hourly data to daily aggregates
	 */
	async compactHourToDay() {
		// get hour data query for batching
		const batchQuery = this.insightsByPeriodRepository.getPeriodInsightsBatchQuery({
			periodUnitToCompactFrom: 'hour',
			compactionBatchSize: this.insightsConfig.compactionBatchSize,
			maxAgeInDays: this.insightsConfig.compactionHourlyToDailyThresholdDays,
		});

		return await this.insightsByPeriodRepository.compactSourceDataIntoInsightPeriod({
			sourceBatchQuery: batchQuery,
			periodUnitToCompactInto: 'day',
		});
	}

	/**
	 * Compacts daily data to weekly aggregates
	 */
	async compactDayToWeek() {
		// get daily data query for batching
		const batchQuery = this.insightsByPeriodRepository.getPeriodInsightsBatchQuery({
			periodUnitToCompactFrom: 'day',
			compactionBatchSize: this.insightsConfig.compactionBatchSize,
			maxAgeInDays: this.insightsConfig.compactionDailyToWeeklyThresholdDays,
		});

		return await this.insightsByPeriodRepository.compactSourceDataIntoInsightPeriod({
			sourceBatchQuery: batchQuery,
			periodUnitToCompactInto: 'week',
		});
	}
}
