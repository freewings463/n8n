"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/repositories/workflow-statistics.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/repositories 的工作流仓储。导入/依赖:外部:无；内部:@n8n/config、@n8n/di、@n8n/permissions；本地:../entities、../entities/types-db。导出:WorkflowStatisticsRepository。关键函数/方法:insertWorkflowStatistics、upsertWorkflowStatistics、VALUES、queryResult、queryNumWorkflowsUserHasWithFiveOrMoreProdExecs。用于封装工作流数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/repositories/workflow-statistics.repository.ts -> services/n8n/infrastructure/n8n-db/persistence/repositories/workflow_statistics_repository.py

import { GlobalConfig } from '@n8n/config';
import { Service } from '@n8n/di';
import { PROJECT_OWNER_ROLE_SLUG } from '@n8n/permissions';
import {
	DataSource,
	IsNull,
	MoreThanOrEqual,
	Not,
	QueryFailedError,
	Repository,
} from '@n8n/typeorm';

import { WorkflowStatistics } from '../entities';
import type { User } from '../entities';
import { StatisticsNames } from '../entities/types-db';

type StatisticsInsertResult = 'insert' | 'failed' | 'alreadyExists';
type StatisticsUpsertResult = StatisticsInsertResult | 'update';

@Service()
export class WorkflowStatisticsRepository extends Repository<WorkflowStatistics> {
	constructor(
		dataSource: DataSource,
		private readonly globalConfig: GlobalConfig,
	) {
		super(WorkflowStatistics, dataSource.manager);
	}

	async insertWorkflowStatistics(
		eventName: StatisticsNames,
		workflowId: string,
	): Promise<StatisticsInsertResult> {
		// Try to insert the data loaded statistic
		try {
			const exists = await this.findOne({
				where: {
					workflowId,
					name: eventName,
				},
			});
			if (exists) return 'alreadyExists';
			await this.insert({
				workflowId,
				name: eventName,
				count: 1,
				rootCount: 1,
				latestEvent: new Date(),
			});
			return 'insert';
		} catch (error) {
			// if it's a duplicate key error then that's fine, otherwise throw the error
			if (!(error instanceof QueryFailedError)) {
				throw error;
			}
			// If it is a query failed error, we return
			return 'failed';
		}
	}

	async upsertWorkflowStatistics(
		eventName: StatisticsNames,
		workflowId: string,
		isRootExecution: boolean,
	): Promise<StatisticsUpsertResult> {
		const dbType = this.globalConfig.database.type;
		const escapedTableName = this.manager.connection.driver.escape(this.metadata.tableName);

		try {
			const rootCountIncrement = isRootExecution ? 1 : 0;
			if (dbType === 'sqlite') {
				await this.query(
					`INSERT INTO ${escapedTableName} ("count", "rootCount", "name", "workflowId", "latestEvent")
					VALUES (1, ?, ?, ?, CURRENT_TIMESTAMP)
					ON CONFLICT (workflowId, name)
					DO UPDATE SET
						count = count + 1,
						rootCount = rootCount + ?,
						latestEvent = CURRENT_TIMESTAMP`,
					[rootCountIncrement, eventName, workflowId, rootCountIncrement],
				);

				// SQLite does not offer a reliable way to know whether or not an insert or update happened.
				// We'll use a naive approach in this case. Query again after and it might cause us to miss the
				// first production execution sometimes due to concurrency, but it's the only way.
				const counter = await this.findOne({
					select: ['count'],
					where: { name: eventName, workflowId },
				});

				return (counter?.count ?? 0) > 1 ? 'update' : counter?.count === 1 ? 'insert' : 'failed';
			} else if (dbType === 'postgresdb') {
				const queryResult = (await this.query(
					`INSERT INTO ${escapedTableName} ("count", "rootCount", "name", "workflowId", "latestEvent")
					VALUES (1, $1, $2, $3, CURRENT_TIMESTAMP)
					ON CONFLICT ("name", "workflowId")
					DO UPDATE SET
						"count" = ${escapedTableName}."count" + 1,
						"rootCount" = ${escapedTableName}."rootCount" + $4,
						"latestEvent" = CURRENT_TIMESTAMP
					RETURNING *;`,
					[rootCountIncrement, eventName, workflowId, rootCountIncrement],
				)) as Array<{ count: number }>;

				return queryResult[0].count === 1 ? 'insert' : 'update';
			} else {
				const queryResult = (await this.query(
					`INSERT INTO ${escapedTableName} (count, rootCount, name, workflowId, latestEvent)
					VALUES (1, ?, ?, ?, NOW())
					ON DUPLICATE KEY
					UPDATE
						count = count + 1,
						rootCount = rootCount + ?,
						latestEvent = NOW();`,
					[rootCountIncrement, eventName, workflowId, rootCountIncrement],
				)) as { affectedRows: number };

				// MySQL returns 2 affected rows on update
				return queryResult.affectedRows === 1 ? 'insert' : 'update';
			}
		} catch (error) {
			console.log('error', error);
			if (error instanceof QueryFailedError) return 'failed';
			throw error;
		}
	}

	async queryNumWorkflowsUserHasWithFiveOrMoreProdExecs(userId: User['id']): Promise<number> {
		return await this.count({
			where: {
				workflow: {
					shared: {
						role: 'workflow:owner',
						project: { projectRelations: { userId, role: { slug: PROJECT_OWNER_ROLE_SLUG } } },
					},
					activeVersionId: Not(IsNull()),
				},
				name: StatisticsNames.productionSuccess,
				count: MoreThanOrEqual(5),
			},
		});
	}
}
