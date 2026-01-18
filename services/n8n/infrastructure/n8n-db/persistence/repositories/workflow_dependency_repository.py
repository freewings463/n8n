"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/repositories/workflow-dependency.repository.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/repositories 的工作流仓储。导入/依赖:外部:无；内部:@n8n/config、@n8n/di、@n8n/typeorm；本地:../entities。导出:WorkflowDependencies、WorkflowDependencyRepository。关键函数/方法:add、updateDependenciesForWorkflow、executeUpdate、removeDependenciesForWorkflow、acquireLockAndCheckForExistingData、getTableName。用于封装工作流数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/repositories/workflow-dependency.repository.ts -> services/n8n/infrastructure/n8n-db/persistence/repositories/workflow_dependency_repository.py

import { DatabaseConfig } from '@n8n/config';
import { Service } from '@n8n/di';
import { DataSource, EntityManager, LessThan, Repository } from '@n8n/typeorm';

import { WorkflowDependency } from '../entities';

const INDEX_VERSION_ID = 1;

/**
 * Helper class to collect workflow dependencies before writing them to the database.
 */
export class WorkflowDependencies {
	readonly dependencies: WorkflowDependency[] = [];

	constructor(
		readonly workflowId: string,
		readonly workflowVersionId: number | undefined,
	) {}

	add(dependency: {
		dependencyType: string;
		dependencyKey: string | null;
		dependencyInfo: Record<string, unknown> | null;
	}) {
		const dep = new WorkflowDependency();
		Object.assign(dep, dependency);
		Object.assign(dep, {
			workflowId: this.workflowId,
			workflowVersionId: this.workflowVersionId,
			indexVersionId: INDEX_VERSION_ID,
		});
		this.dependencies.push(dep);
	}
}

@Service()
export class WorkflowDependencyRepository extends Repository<WorkflowDependency> {
	constructor(
		dataSource: DataSource,
		private readonly databaseConfig: DatabaseConfig,
	) {
		super(WorkflowDependency, dataSource.manager);
	}
	/**
	 * Replace the dependencies for a given workflow.
	 * Uses the workflowVersionId to ensure consistency between the workflow and dependency tables.
	 * @param workflowId the id of the workflow
	 * @param dependencies the new dependencies to be written
	 * @returns whether the update was applied
	 */
	async updateDependenciesForWorkflow(
		workflowId: string,
		dependencies: WorkflowDependencies,
	): Promise<boolean> {
		if (this.databaseConfig.isLegacySqlite) {
			throw new Error('Workflow dependency indexing is not supported on legacy SQLite databases');
		}
		return await this.manager.transaction(async (tx) => {
			return await this.executeUpdate(workflowId, dependencies, tx);
		});
	}

	private async executeUpdate(
		workflowId: string,
		dependencies: WorkflowDependencies,
		tx: EntityManager,
	): Promise<boolean> {
		const deleteResult = await tx.delete(WorkflowDependency, {
			workflowId,
			workflowVersionId: LessThan(dependencies.workflowVersionId),
		});

		// If we deleted something, the incoming version is newer - proceed with insert
		if (deleteResult.affected && deleteResult.affected > 0) {
			// NOTE: we cast to any[] because TypeORM doesn't like the JSON column.
			// eslint-disable-next-line @typescript-eslint/no-explicit-any
			await tx.insert(WorkflowDependency, dependencies.dependencies as any[]);
			return true;
		}

		// Nothing was deleted - either no existing data, or existing data is newer/same version
		// Check if any dependencies exist for this workflow. We lock for update to avoid a race
		// when two processes try to insert dependencies for the same workflow at the same time.
		const hasData = await this.acquireLockAndCheckForExistingData(workflowId, tx);

		if (!hasData) {
			// There's no existing data, so we can safely insert the new dependencies.
			const entities = dependencies.dependencies.map((dep) => this.create(dep));
			// NOTE: we cast to any[] because TypeORM doesn't like the JSON column.
			// eslint-disable-next-line @typescript-eslint/no-explicit-any
			await tx.insert(WorkflowDependency, entities as any[]);
			return true;
		}

		// Existing data has same or newer version - skip update
		return false;
	}

	/**
	 * Remove all dependencies for a given workflow.
	 *
	 * NOTE: there's a possible race in case of an update and delete happening concurrently.
	 * The delete could be reflected in the database, but the update could be reflected in the index.
	 * To prevent this we would need to implement some tombstone mechanism. However, since we don't
	 * do this for the workflow itself, it would be inconsistent to do it only for the dependencies.
	 * The chance of this happening in practice is also very low.
	 *
	 * @param workflowId The ID of the workflow
	 * @returns Whether any dependencies were removed
	 */
	async removeDependenciesForWorkflow(workflowId: string): Promise<boolean> {
		if (this.databaseConfig.isLegacySqlite) {
			throw new Error('Workflow dependency indexing is not supported on legacy SQLite databases');
		}
		return await this.manager.transaction(async (tx) => {
			const deleteResult = await tx.delete(WorkflowDependency, { workflowId });

			return (
				deleteResult.affected !== undefined &&
				deleteResult.affected !== null &&
				deleteResult.affected > 0
			);
		});
	}

	private async acquireLockAndCheckForExistingData(
		workflowId: string,
		tx: EntityManager,
	): Promise<boolean> {
		if (this.databaseConfig.type === 'sqlite') {
			// We skip the explicit locking here. SQLite locks the entire database for writes,
			// so the prepareTransactionForSqlite step ensures no concurrent writes happen.
			return await tx.existsBy(WorkflowDependency, { workflowId });
		}
		// For Postgres and MySQL we lock on the workflow row, and only then check the dependency table.
		// This prevents a race between two concurrent updates.
		const placeholder = this.databaseConfig.type === 'postgresdb' ? '$1' : '?';
		const tableName = this.getTableName('workflow_entity');
		await tx.query(`SELECT id FROM ${tableName} WHERE id = ${placeholder} FOR UPDATE`, [
			workflowId,
		]);
		return await tx.existsBy(WorkflowDependency, { workflowId });
	}

	private getTableName(name: string): string {
		const { tablePrefix } = this.databaseConfig;
		return this.manager.connection.driver.escape(`${tablePrefix}${name}`);
	}
}
