"""
MIGRATION-META:
  source_path: packages/cli/src/controllers/orchestration.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/controllers 的控制器。导入/依赖:外部:无；内部:@n8n/decorators、@/license、@/scaling/worker-status.service.ee；本地:无。导出:OrchestrationController。关键函数/方法:getWorkersStatusAll。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected @RestController/@Controller from @n8n/decorators
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/controllers/orchestration.controller.ts -> services/n8n/presentation/cli/api/v1/controllers/orchestration_controller.py

import { Post, RestController, GlobalScope } from '@n8n/decorators';

import { License } from '@/license';
import { WorkerStatusService } from '@/scaling/worker-status.service.ee';

@RestController('/orchestration')
export class OrchestrationController {
	constructor(
		private readonly licenseService: License,
		private readonly workerStatusService: WorkerStatusService,
	) {}

	/**
	 * This endpoint does not return anything, it just triggers the message to
	 * the workers to respond on Redis with their status.
	 */
	@GlobalScope('orchestration:read')
	@Post('/worker/status')
	async getWorkersStatusAll() {
		if (!this.licenseService.isWorkerViewLicensed()) return;

		return await this.workerStatusService.requestWorkerStatus();
	}
}
