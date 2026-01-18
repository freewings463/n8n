"""
MIGRATION-META:
  source_path: packages/cli/src/controllers/active-workflows.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/controllers 的工作流控制器。导入/依赖:外部:无；内部:@n8n/decorators、@/requests、@/services/active-workflows.service；本地:无。导出:ActiveWorkflowsController。关键函数/方法:getActiveWorkflows、getActivationError。用于处理工作流接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected @RestController/@Controller from @n8n/decorators
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/controllers/active-workflows.controller.ts -> services/n8n/presentation/cli/api/v1/controllers/active_workflows_controller.py

import { Get, RestController } from '@n8n/decorators';

import { ActiveWorkflowRequest } from '@/requests';
import { ActiveWorkflowsService } from '@/services/active-workflows.service';

@RestController('/active-workflows')
export class ActiveWorkflowsController {
	constructor(private readonly activeWorkflowsService: ActiveWorkflowsService) {}

	@Get('/')
	async getActiveWorkflows(req: ActiveWorkflowRequest.GetAllActive) {
		return await this.activeWorkflowsService.getAllActiveIdsFor(req.user);
	}

	@Get('/error/:id')
	async getActivationError(req: ActiveWorkflowRequest.GetActivationError) {
		const {
			user,
			params: { id: workflowId },
		} = req;
		return await this.activeWorkflowsService.getActivationError(workflowId, user);
	}
}
