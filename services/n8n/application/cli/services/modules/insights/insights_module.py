"""
MIGRATION-META:
  source_path: packages/cli/src/modules/insights/insights.module.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/insights 的Insights模块。导入/依赖:外部:无；内部:@n8n/decorators、@n8n/di；本地:./insights.controller、./insights.service、../entities/insights-by-period、../entities/insights-metadata 等2项。导出:InsightsModule。关键函数/方法:init、entities、settings、shutdown。用于承载Insights实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/insights/insights.module.ts -> services/n8n/application/cli/services/modules/insights/insights_module.py

import type { ModuleInterface } from '@n8n/decorators';
import { BackendModule, OnShutdown } from '@n8n/decorators';
import { Container } from '@n8n/di';

/**
 * Only main- and webhook-type instances collect insights because
 * only they are informed of finished workflow executions.
 */
@BackendModule({ name: 'insights', instanceTypes: ['main', 'webhook'] })
export class InsightsModule implements ModuleInterface {
	async init() {
		await import('./insights.controller');

		const { InsightsService } = await import('./insights.service');
		await Container.get(InsightsService).init();
	}

	async entities() {
		const { InsightsByPeriod } = await import('./database/entities/insights-by-period');
		const { InsightsMetadata } = await import('./database/entities/insights-metadata');
		const { InsightsRaw } = await import('./database/entities/insights-raw');

		return [InsightsByPeriod, InsightsMetadata, InsightsRaw];
	}

	async settings() {
		const { InsightsSettings } = await import('./insights.settings');

		return Container.get(InsightsSettings).settings();
	}

	@OnShutdown()
	async shutdown() {
		const { InsightsService } = await import('./insights.service');

		await Container.get(InsightsService).shutdown();
	}
}
