"""
MIGRATION-META:
  source_path: packages/cli/src/controllers/debug.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/controllers 的控制器。导入/依赖:外部:无；内部:@n8n/db、@n8n/decorators、n8n-core、@/active-workflow-manager、@/scaling/multi-main-setup.ee；本地:无。导出:DebugController。关键函数/方法:getMultiMainSetupDetails。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected @RestController/@Controller from @n8n/decorators
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/controllers/debug.controller.ts -> services/n8n/presentation/cli/api/v1/controllers/debug_controller.py

import { WorkflowRepository } from '@n8n/db';
import { Get, RestController } from '@n8n/decorators';
import { InstanceSettings } from 'n8n-core';

import { ActiveWorkflowManager } from '@/active-workflow-manager';
import { MultiMainSetup } from '@/scaling/multi-main-setup.ee';

@RestController('/debug')
export class DebugController {
	constructor(
		private readonly multiMainSetup: MultiMainSetup,
		private readonly activeWorkflowManager: ActiveWorkflowManager,
		private readonly workflowRepository: WorkflowRepository,
		private readonly instanceSettings: InstanceSettings,
	) {}

	@Get('/multi-main-setup', { skipAuth: true })
	async getMultiMainSetupDetails() {
		const leaderKey = await this.multiMainSetup.fetchLeaderKey();

		const triggersAndPollers = await this.workflowRepository.findIn(
			this.activeWorkflowManager.allActiveInMemory(),
		);

		const webhooks = await this.workflowRepository.findWebhookBasedActiveWorkflows();

		const activationErrors = await this.activeWorkflowManager.getAllWorkflowActivationErrors();

		return {
			instanceId: this.instanceSettings.instanceId,
			leaderKey,
			isLeader: this.instanceSettings.isLeader,
			activeWorkflows: {
				webhooks, // webhook-based active workflows
				triggersAndPollers, // poller- and trigger-based active workflows
			},
			activationErrors,
		};
	}
}
