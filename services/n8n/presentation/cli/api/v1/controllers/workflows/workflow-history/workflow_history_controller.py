"""
MIGRATION-META:
  source_path: packages/cli/src/workflows/workflow-history/workflow-history.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/workflows/workflow-history 的工作流控制器。导入/依赖:外部:无；内部:@n8n/api-types、@n8n/decorators、@/errors/…/not-found.error、@/errors/shared-workflow-not-found.error、@/errors/workflow-history-version-not-found.error、@/requests；本地:./workflow-history.service。导出:WorkflowHistoryController。关键函数/方法:getList、getVersion、getVersionsByIds。用于处理工作流接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected @RestController/@Controller from @n8n/decorators
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/workflows/workflow-history/workflow-history.controller.ts -> services/n8n/presentation/cli/api/v1/controllers/workflows/workflow-history/workflow_history_controller.py

import { PaginationDto, WorkflowHistoryVersionsByIdsDto } from '@n8n/api-types';
import { RestController, Get, Post, Query, Body } from '@n8n/decorators';

import { NotFoundError } from '@/errors/response-errors/not-found.error';
import { SharedWorkflowNotFoundError } from '@/errors/shared-workflow-not-found.error';
import { WorkflowHistoryVersionNotFoundError } from '@/errors/workflow-history-version-not-found.error';
import { WorkflowHistoryRequest } from '@/requests';

import { WorkflowHistoryService } from './workflow-history.service';

const DEFAULT_TAKE = 20;

@RestController('/workflow-history')
export class WorkflowHistoryController {
	constructor(private readonly historyService: WorkflowHistoryService) {}

	@Get('/workflow/:workflowId')
	async getList(req: WorkflowHistoryRequest.GetList, _res: Response, @Query query: PaginationDto) {
		try {
			return await this.historyService.getList(
				req.user,
				req.params.workflowId,
				query.take ?? DEFAULT_TAKE,
				query.skip ?? 0,
			);
		} catch (e) {
			if (e instanceof SharedWorkflowNotFoundError) {
				throw new NotFoundError('Could not find workflow');
			}
			throw e;
		}
	}

	@Get('/workflow/:workflowId/version/:versionId')
	async getVersion(req: WorkflowHistoryRequest.GetVersion) {
		try {
			return await this.historyService.getVersion(
				req.user,
				req.params.workflowId,
				req.params.versionId,
			);
		} catch (e) {
			if (e instanceof SharedWorkflowNotFoundError) {
				throw new NotFoundError('Could not find workflow');
			} else if (e instanceof WorkflowHistoryVersionNotFoundError) {
				throw new NotFoundError('Could not find version');
			}
			throw e;
		}
	}

	@Post('/workflow/:workflowId/versions')
	async getVersionsByIds(
		req: WorkflowHistoryRequest.GetList,
		_res: Response,
		@Body body: WorkflowHistoryVersionsByIdsDto,
	) {
		try {
			const versions = await this.historyService.getVersionsByIds(
				req.user,
				req.params.workflowId,
				body.versionIds,
			);
			return { versions };
		} catch (e) {
			if (e instanceof SharedWorkflowNotFoundError) {
				throw new NotFoundError('Could not find workflow');
			}
			throw e;
		}
	}
}
