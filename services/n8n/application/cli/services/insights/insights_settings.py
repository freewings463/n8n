"""
MIGRATION-META:
  source_path: packages/cli/src/modules/insights/insights.settings.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/insights 的Insights模块。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/di；本地:./insights.constants。导出:InsightsSettings。关键函数/方法:settings、getAvailableDateRanges。用于承载Insights实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/insights/insights.settings.ts -> services/n8n/application/cli/services/insights/insights_settings.py

import { LicenseState } from '@n8n/backend-common';
import { Service } from '@n8n/di';

import { INSIGHTS_DATE_RANGE_KEYS, keyRangeToDays } from './insights.constants';

@Service()
export class InsightsSettings {
	constructor(private readonly licenseState: LicenseState) {}

	settings() {
		return {
			summary: this.licenseState.isInsightsSummaryLicensed(),
			dashboard: this.licenseState.isInsightsDashboardLicensed(),
			dateRanges: this.getAvailableDateRanges(),
		};
	}

	private getAvailableDateRanges(): DateRange[] {
		const maxHistoryInDays =
			this.licenseState.getInsightsMaxHistory() === -1
				? Number.MAX_SAFE_INTEGER
				: this.licenseState.getInsightsMaxHistory();
		const isHourlyDateLicensed = this.licenseState.isInsightsHourlyDataLicensed();

		return INSIGHTS_DATE_RANGE_KEYS.map((key) => ({
			key,
			licensed:
				key === 'day' ? (isHourlyDateLicensed ?? false) : maxHistoryInDays >= keyRangeToDays[key],
			granularity: key === 'day' ? 'hour' : keyRangeToDays[key] <= 30 ? 'day' : 'week',
		}));
	}
}

type DateRange = {
	key: 'day' | 'week' | '2weeks' | 'month' | 'quarter' | '6months' | 'year';
	licensed: boolean;
	granularity: 'hour' | 'day' | 'week';
};
