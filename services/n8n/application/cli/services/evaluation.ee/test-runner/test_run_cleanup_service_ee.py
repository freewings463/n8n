"""
MIGRATION-META:
  source_path: packages/cli/src/evaluation.ee/test-runner/test-run-cleanup.service.ee.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/evaluation.ee/test-runner 的服务。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/db、@n8n/di；本地:无。导出:TestRunCleanupService。关键函数/方法:cleanupIncompleteRuns。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/evaluation.ee/test-runner/test-run-cleanup.service.ee.ts -> services/n8n/application/cli/services/evaluation.ee/test-runner/test_run_cleanup_service_ee.py

import { Logger } from '@n8n/backend-common';
import { TestRunRepository } from '@n8n/db';
import { Service } from '@n8n/di';

/**
 * This service is responsible for cleaning up pending Test Runs on application startup.
 */
@Service()
export class TestRunCleanupService {
	constructor(
		private readonly logger: Logger,
		private readonly testRunRepository: TestRunRepository,
	) {}

	/**
	 * As Test Runner does not have a recovery mechanism, it can not resume Test Runs interrupted by the server restart.
	 * All Test Runs in incomplete state will be marked as failed.
	 */
	async cleanupIncompleteRuns() {
		const result = await this.testRunRepository.markAllIncompleteAsFailed();
		if (result.affected && result.affected > 0) {
			this.logger.debug(`Marked ${result.affected} incomplete test runs as failed`);
		}
	}
}
