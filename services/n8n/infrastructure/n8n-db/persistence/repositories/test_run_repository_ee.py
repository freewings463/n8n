"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/repositories/test-run.repository.ee.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/repositories 的仓储。导入/依赖:外部:无；内部:@n8n/di、@n8n/typeorm、n8n-workflow；本地:../entities、../utils/get-final-test-result。导出:TestRunSummary、TestRunRepository。关键函数/方法:createTestRun、markAsRunning、markAsCompleted、markAsCancelled、markAsError、markAllIncompleteAsFailed、getMany、getTestRunSummaryById。用于封装该模块数据读写与查询细节，隔离持久层。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/repositories/test-run.repository.ee.ts -> services/n8n/infrastructure/n8n-db/persistence/repositories/test_run_repository_ee.py

import { Service } from '@n8n/di';
import type { EntityManager, FindManyOptions } from '@n8n/typeorm';
import { DataSource, In, Repository } from '@n8n/typeorm';
import { UnexpectedError, type IDataObject } from 'n8n-workflow';

import { TestRun } from '../entities';
import type {
	AggregatedTestRunMetrics,
	TestRunErrorCode,
	TestRunFinalResult,
	ListQuery,
} from '../entities/types-db';
import { getTestRunFinalResult } from '../utils/get-final-test-result';

export type TestRunSummary = TestRun & {
	finalResult: TestRunFinalResult | null;
};

@Service()
export class TestRunRepository extends Repository<TestRun> {
	constructor(dataSource: DataSource) {
		super(TestRun, dataSource.manager);
	}

	async createTestRun(workflowId: string): Promise<TestRun> {
		const testRun = this.create({
			status: 'new',
			workflow: {
				id: workflowId,
			},
		});

		return await this.save(testRun);
	}

	async markAsRunning(id: string) {
		return await this.update(id, {
			status: 'running',
			runAt: new Date(),
		});
	}

	async markAsCompleted(id: string, metrics: AggregatedTestRunMetrics) {
		return await this.update(id, { status: 'completed', completedAt: new Date(), metrics });
	}

	async markAsCancelled(id: string, trx?: EntityManager) {
		trx = trx ?? this.manager;
		return await trx.update(TestRun, id, { status: 'cancelled', completedAt: new Date() });
	}

	async markAsError(id: string, errorCode: TestRunErrorCode, errorDetails?: IDataObject) {
		return await this.update(id, {
			status: 'error',
			errorCode,
			errorDetails,
			completedAt: new Date(),
		});
	}

	async markAllIncompleteAsFailed() {
		return await this.update(
			{ status: In(['new', 'running']) },
			{ status: 'error', errorCode: 'INTERRUPTED', completedAt: new Date() },
		);
	}

	async getMany(workflowId: string, options: ListQuery.Options) {
		// FIXME: optimize fetching final result of each test run
		const findManyOptions: FindManyOptions<TestRun> = {
			where: { workflow: { id: workflowId } },
			order: { createdAt: 'DESC' },
			relations: ['testCaseExecutions'],
		};

		if (options?.take) {
			findManyOptions.skip = options.skip;
			findManyOptions.take = options.take;
		}

		const testRuns = await this.find(findManyOptions);

		return testRuns.map(({ testCaseExecutions, ...testRun }) => {
			const finalResult =
				testRun.status === 'completed' ? getTestRunFinalResult(testCaseExecutions) : null;
			return { ...testRun, finalResult };
		});
	}

	/**
	 * Test run summary is a TestRun with a final result.
	 * Final result is calculated based on the status of all test case executions.
	 * E.g. Test Run is considered successful if all test case executions are successful.
	 * Test Run is considered failed if at least one test case execution is failed.
	 */
	async getTestRunSummaryById(testRunId: string): Promise<TestRunSummary> {
		const testRun = await this.findOne({
			where: { id: testRunId },
			relations: ['testCaseExecutions'],
		});

		if (!testRun) {
			throw new UnexpectedError('Test run not found');
		}

		testRun.finalResult =
			testRun.status === 'completed' ? getTestRunFinalResult(testRun.testCaseExecutions) : null;

		return testRun as TestRunSummary;
	}
}
