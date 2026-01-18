"""
MIGRATION-META:
  source_path: packages/cli/src/modules/breaking-changes/breaking-changes.controller.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/modules/breaking-changes 的控制器。导入/依赖:外部:无；内部:@n8n/db、@n8n/decorators、@/errors/…/not-found.error；本地:./breaking-changes.service。导出:BreakingChangesController。关键函数/方法:getLightDetectionResults、getDetectionReport、refreshCache、getDetectionReportForRule。用于处理该模块接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected @RestController/@Controller from @n8n/decorators
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/breaking-changes/breaking-changes.controller.ts -> services/n8n/presentation/cli/api/v1/controllers/modules/breaking-changes/breaking_changes_controller.py

import {
	BreakingChangeInstanceRuleResult,
	BreakingChangeLightReportResult,
	BreakingChangeReportResult,
	BreakingChangeVersion,
	BreakingChangeWorkflowRuleResult,
} from '@n8n/api-types';
import { AuthenticatedRequest } from '@n8n/db';
import { Get, RestController, GlobalScope, Query, Post, Param } from '@n8n/decorators';

import { BreakingChangeService } from './breaking-changes.service';

import { NotFoundError } from '@/errors/response-errors/not-found.error';

@RestController('/breaking-changes')
export class BreakingChangesController {
	constructor(private readonly service: BreakingChangeService) {}

	private getLightDetectionResults(
		report: BreakingChangeReportResult['report'],
	): BreakingChangeLightReportResult['report'] {
		return {
			...report,
			workflowResults: report.workflowResults.map((r) => {
				const { affectedWorkflows, ...otherFields } = r;
				return { ...otherFields, nbAffectedWorkflows: affectedWorkflows.length };
			}),
		};
	}

	/**
	 * Get all registered breaking change rules results
	 */
	@Get('/report')
	@GlobalScope('breakingChanges:list')
	async getDetectionReport(
		@Query query: { version?: BreakingChangeVersion },
	): Promise<BreakingChangeLightReportResult> {
		const report = await this.service.getDetectionResults(query.version ?? 'v2');
		return {
			...report,
			report: this.getLightDetectionResults(report.report),
		};
	}

	@Post('/report/refresh')
	@GlobalScope('breakingChanges:list')
	async refreshCache(
		@Query query: { version?: BreakingChangeVersion },
	): Promise<BreakingChangeLightReportResult> {
		const report = await this.service.refreshDetectionResults(query.version ?? 'v2');
		return {
			...report,
			report: this.getLightDetectionResults(report.report),
		};
	}

	/**
	 * Get specific breaking change rules
	 */
	@Get('/report/:ruleId')
	@GlobalScope('breakingChanges:list')
	async getDetectionReportForRule(
		_req: AuthenticatedRequest,
		_res: Response,
		@Param('ruleId') ruleId: string,
	): Promise<BreakingChangeInstanceRuleResult | BreakingChangeWorkflowRuleResult> {
		const result = await this.service.getDetectionReportForRule(ruleId);
		if (!result) {
			throw new NotFoundError(`Breaking change rule with ID '${ruleId}' not found.`);
		}
		return result;
	}
}
