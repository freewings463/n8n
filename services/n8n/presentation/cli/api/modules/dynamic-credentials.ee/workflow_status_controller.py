"""
MIGRATION-META:
  source_path: packages/cli/src/modules/dynamic-credentials.ee/workflow-status.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/dynamic-credentials.ee 的工作流控制器。导入/依赖:外部:express；内部:@n8n/decorators、@/errors/…/bad-request.error、@n8n/api-types、@/services/url.service、@n8n/config；本地:./services/credential-resolver-workflow.service、./utils。导出:WorkflowStatusController。关键函数/方法:checkWorkflowForExecution。用于处理工作流接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/dynamic-credentials.ee/workflow-status.controller.ts -> services/n8n/presentation/cli/api/modules/dynamic-credentials.ee/workflow_status_controller.py

import { Get, RestController } from '@n8n/decorators';
import { Request, Response } from 'express';

import { BadRequestError } from '@/errors/response-errors/bad-request.error';
import { CredentialResolverWorkflowService } from './services/credential-resolver-workflow.service';
import { WorkflowExecutionStatus } from '@n8n/api-types';
import { getBearerToken } from './utils';
import { UrlService } from '@/services/url.service';
import { GlobalConfig } from '@n8n/config';

@RestController('/workflows')
export class WorkflowStatusController {
	constructor(
		private readonly credentialResolverWorkflowService: CredentialResolverWorkflowService,
		private readonly urlService: UrlService,
		private readonly globalConfig: GlobalConfig,
	) {}

	/**
	 * GET /workflows/:workflowId/execution-status
	 *
	 * Checks if a workflow is ready to execute by validating all resolvable credentials.
	 * Requires Bearer token authentication in Authorization header.
	 *
	 * @returns Workflow execution status with credential details and authorization URLs
	 * @throws {BadRequestError} When authorization header is missing or malformed
	 */
	@Get('/:workflowId/execution-status', { skipAuth: true })
	async checkWorkflowForExecution(req: Request, _res: Response): Promise<WorkflowExecutionStatus> {
		const workflowId = req.params['workflowId'];
		const token = getBearerToken(req);

		if (!workflowId) {
			throw new BadRequestError('Workflow ID is missing');
		}

		const status = await this.credentialResolverWorkflowService.getWorkflowStatus(
			workflowId,
			token,
		);

		const isReady = status.every((s) => s.status === 'configured');

		const basePath = this.urlService.getInstanceBaseUrl();
		const restPath = this.globalConfig.endpoints.rest;

		const executionStatus: WorkflowExecutionStatus = {
			workflowId,
			readyToExecute: isReady,
			credentials: status.map((s) => ({
				credentialId: s.credentialId,
				credentialName: s.credentialName,
				credentialStatus: s.status,
				credentialType: s.credentialType,
				authorizationUrl: `${basePath}/${restPath}/credentials/${s.credentialId}/authorize?resolverId=${encodeURIComponent(s.resolverId)}`,
			})),
		};
		return executionStatus;
	}
}
