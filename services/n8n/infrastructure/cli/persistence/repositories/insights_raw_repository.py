"""
MIGRATION-META:
  source_path: packages/cli/src/modules/insights/database/repositories/insights-raw.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/insights/database 的Insights仓储。导入/依赖:外部:无；内部:@n8n/di、@n8n/typeorm；本地:../entities/insights-raw。导出:InsightsRawRepository。关键函数/方法:getRawInsightsBatchQuery。用于封装Insights数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/insights/database/repositories/insights-raw.repository.ts -> services/n8n/infrastructure/cli/persistence/repositories/insights_raw_repository.py

import { Service } from '@n8n/di';
import { DataSource, Repository } from '@n8n/typeorm';

import { InsightsRaw } from '../entities/insights-raw';

@Service()
export class InsightsRawRepository extends Repository<InsightsRaw> {
	constructor(dataSource: DataSource) {
		super(InsightsRaw, dataSource.manager);
	}

	getRawInsightsBatchQuery(compactionBatchSize: number) {
		// Build the query to gather raw insights data for the batch
		const batchQuery = this.manager
			.createQueryBuilder<{
				id: number;
				metaId: number;
				type: string;
				value: number;
				periodStart: Date;
			}>(InsightsRaw, 'insightsRaw')
			.select(
				['id', 'metaId', 'type', 'value'].map((fieldName) =>
					this.manager.connection.driver.escape(fieldName),
				),
			)
			.addSelect('timestamp', 'periodStart')
			.orderBy('timestamp', 'ASC')
			.limit(compactionBatchSize);

		return batchQuery;
	}
}
