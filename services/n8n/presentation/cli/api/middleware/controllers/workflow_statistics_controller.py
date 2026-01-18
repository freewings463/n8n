"""
MIGRATION-META:
  source_path: packages/cli/src/controllers/workflow-statistics.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/controllers 的工作流控制器。导入/依赖:外部:express；内部:@n8n/backend-common、@n8n/db、@n8n/decorators、@/errors/…/not-found.error、@/interfaces、@/workflows/workflow-finder.service；本地:./workflow-statistics.types。导出:WorkflowStatisticsController。关键函数/方法:hasWorkflowAccess、next、getCounts、getTimes、getDataLoaded。用于处理工作流接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected Express RequestHandler-style middleware
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/controllers/workflow-statistics.controller.ts -> services/n8n/presentation/cli/api/middleware/controllers/workflow_statistics_controller.py

import { Logger } from '@n8n/backend-common';
import type { WorkflowStatistics } from '@n8n/db';
import { StatisticsNames, WorkflowStatisticsRepository } from '@n8n/db';
import { Get, Middleware, RestController } from '@n8n/decorators';
import { Response, NextFunction } from 'express';

import { NotFoundError } from '@/errors/response-errors/not-found.error';
import type { IWorkflowStatisticsDataLoaded } from '@/interfaces';
import { WorkflowFinderService } from '@/workflows/workflow-finder.service';

import { StatisticsRequest } from './workflow-statistics.types';

interface WorkflowStatisticsData<T> {
	productionSuccess: T;
	productionError: T;
	manualSuccess: T;
	manualError: T;
}

@RestController('/workflow-stats')
export class WorkflowStatisticsController {
	constructor(
		private readonly workflowFinderService: WorkflowFinderService,
		private readonly workflowStatisticsRepository: WorkflowStatisticsRepository,
		private readonly logger: Logger,
	) {}

	/**
	 * Check that the workflow ID is valid and allowed to be read by the user
	 */
	// TODO: move this into a new decorator `@ValidateWorkflowPermission`
	@Middleware()
	async hasWorkflowAccess(req: StatisticsRequest.GetOne, _res: Response, next: NextFunction) {
		const { user } = req;
		const workflowId = req.params.id;

		const workflow = await this.workflowFinderService.findWorkflowForUser(workflowId, user, [
			'workflow:read',
		]);

		if (workflow) {
			next();
		} else {
			this.logger.warn('User attempted to read a workflow without permissions', {
				workflowId,
				userId: user.id,
			});
			// Otherwise, make and return an error
			throw new NotFoundError(`Workflow ${workflowId} does not exist.`);
		}
	}

	@Get('/:id/counts/')
	async getCounts(req: StatisticsRequest.GetOne): Promise<WorkflowStatisticsData<number>> {
		return await this.getData(req.params.id, 'count', 0);
	}

	@Get('/:id/times/')
	async getTimes(req: StatisticsRequest.GetOne): Promise<WorkflowStatisticsData<Date | null>> {
		return await this.getData(req.params.id, 'latestEvent', null);
	}

	@Get('/:id/data-loaded/')
	async getDataLoaded(req: StatisticsRequest.GetOne): Promise<IWorkflowStatisticsDataLoaded> {
		// Get flag
		const workflowId = req.params.id;

		// Get the flag
		const stats = await this.workflowStatisticsRepository.findOne({
			select: ['latestEvent'],
			where: {
				workflowId,
				name: StatisticsNames.dataLoaded,
			},
		});

		return {
			dataLoaded: stats ? true : false,
		};
	}

	private async getData<
		C extends 'count' | 'latestEvent',
		D = WorkflowStatistics[C] extends number ? 0 : null,
	>(workflowId: string, columnName: C, defaultValue: WorkflowStatistics[C] | D) {
		const stats = await this.workflowStatisticsRepository.find({
			select: [columnName, 'name'],
			where: { workflowId },
		});

		const data: WorkflowStatisticsData<WorkflowStatistics[C] | D> = {
			productionSuccess: defaultValue,
			productionError: defaultValue,
			manualSuccess: defaultValue,
			manualError: defaultValue,
		};

		stats.forEach(({ name, [columnName]: value }) => {
			switch (name) {
				case StatisticsNames.manualError:
					data.manualError = value;
					break;

				case StatisticsNames.manualSuccess:
					data.manualSuccess = value;
					break;

				case StatisticsNames.productionError:
					data.productionError = value;
					break;

				case StatisticsNames.productionSuccess:
					data.productionSuccess = value;
			}
		});

		return data;
	}
}
