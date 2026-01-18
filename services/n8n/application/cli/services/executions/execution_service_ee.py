"""
MIGRATION-META:
  source_path: packages/cli/src/executions/execution.service.ee.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/executions 的执行服务。导入/依赖:外部:无；内部:@n8n/db、@n8n/di、@/interfaces；本地:./execution.service、./execution.types、../workflows/workflow.service.ee。导出:EnterpriseExecutionsService。关键函数/方法:findOne、workflow。用于封装执行业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/executions/execution.service.ee.ts -> services/n8n/application/cli/services/executions/execution_service_ee.py

import type { WorkflowWithSharingsAndCredentials, IExecutionResponse } from '@n8n/db';
import { WorkflowRepository } from '@n8n/db';
import { Service } from '@n8n/di';

import type { IExecutionFlattedResponse } from '@/interfaces';

import { ExecutionService } from './execution.service';
import type { ExecutionRequest } from './execution.types';
import { EnterpriseWorkflowService } from '../workflows/workflow.service.ee';

@Service()
export class EnterpriseExecutionsService {
	constructor(
		private readonly executionService: ExecutionService,
		private readonly workflowRepository: WorkflowRepository,
		private readonly enterpriseWorkflowService: EnterpriseWorkflowService,
	) {}

	async findOne(
		req: ExecutionRequest.GetOne,
		sharedWorkflowIds: string[],
	): Promise<IExecutionResponse | IExecutionFlattedResponse | undefined> {
		const execution = await this.executionService.findOne(req, sharedWorkflowIds);

		if (!execution) return;

		const workflow = (await this.workflowRepository.get({
			id: execution.workflowId,
		})) as WorkflowWithSharingsAndCredentials;

		if (!workflow) return;

		const workflowWithSharingsMetaData =
			this.enterpriseWorkflowService.addOwnerAndSharings(workflow);
		await this.enterpriseWorkflowService.addCredentialsToWorkflow(
			workflowWithSharingsMetaData,
			req.user,
		);

		execution.workflowData = {
			...execution.workflowData,
			homeProject: workflowWithSharingsMetaData.homeProject,
			sharedWithProjects: workflowWithSharingsMetaData.sharedWithProjects,
			usedCredentials: workflowWithSharingsMetaData.usedCredentials,
		} as WorkflowWithSharingsAndCredentials;

		return execution;
	}
}
