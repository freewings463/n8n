"""
MIGRATION-META:
  source_path: packages/cli/src/services/workflow-loader.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/services 的工作流服务。导入/依赖:外部:无；内部:@n8n/db、@n8n/di、n8n-workflow；本地:无。导出:WorkflowLoaderService。关键函数/方法:get。用于封装工作流业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/services/workflow-loader.service.ts -> services/n8n/application/cli/services/workflow_loader_service.py

import { WorkflowRepository } from '@n8n/db';
import { Service } from '@n8n/di';
import { UserError, type IWorkflowBase, type IWorkflowLoader } from 'n8n-workflow';

@Service()
export class WorkflowLoaderService implements IWorkflowLoader {
	constructor(private readonly workflowRepository: WorkflowRepository) {}

	async get(workflowId: string): Promise<IWorkflowBase> {
		const workflow = await this.workflowRepository.findById(workflowId);

		if (!workflow) {
			throw new UserError(`Failed to find workflow with ID "${workflowId}"`);
		}

		return workflow;
	}
}
