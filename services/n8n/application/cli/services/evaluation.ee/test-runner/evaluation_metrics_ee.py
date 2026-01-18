"""
MIGRATION-META:
  source_path: packages/cli/src/evaluation.ee/test-runner/evaluation-metrics.ee.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/evaluation.ee/test-runner 的模块。导入/依赖:外部:无；内部:n8n-workflow、@/evaluation.ee/…/errors.ee；本地:无。导出:EvaluationMetricsAddResultsInfo、EvaluationMetrics。关键函数/方法:addResults、getAggregatedMetrics。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/evaluation.ee/test-runner/evaluation-metrics.ee.ts -> services/n8n/application/cli/services/evaluation.ee/test-runner/evaluation_metrics_ee.py

import type { IDataObject } from 'n8n-workflow';

import { TestCaseExecutionError } from '@/evaluation.ee/test-runner/errors.ee';

export interface EvaluationMetricsAddResultsInfo {
	addedMetrics: Record<string, number>;
	incorrectTypeMetrics: Set<string>;
}

export class EvaluationMetrics {
	private readonly rawMetricsByName = new Map<string, number[]>();

	addResults(result: IDataObject): EvaluationMetricsAddResultsInfo {
		const addResultsInfo: EvaluationMetricsAddResultsInfo = {
			addedMetrics: {},
			incorrectTypeMetrics: new Set<string>(),
		};

		for (const [metricName, metricValue] of Object.entries(result)) {
			if (typeof metricValue === 'number') {
				addResultsInfo.addedMetrics[metricName] = metricValue;

				// Initialize the array if this is the first time we see this metric
				if (!this.rawMetricsByName.has(metricName)) {
					this.rawMetricsByName.set(metricName, []);
				}

				this.rawMetricsByName.get(metricName)!.push(metricValue);
			} else {
				addResultsInfo.incorrectTypeMetrics.add(metricName);
				throw new TestCaseExecutionError('INVALID_METRICS', {
					metricName,
					metricValue,
				});
			}
		}

		return addResultsInfo;
	}

	getAggregatedMetrics() {
		const aggregatedMetrics: Record<string, number> = {};

		for (const [metricName, metricValues] of this.rawMetricsByName.entries()) {
			if (metricValues.length > 0) {
				const metricSum = metricValues.reduce((acc, val) => acc + val, 0);
				aggregatedMetrics[metricName] = metricSum / metricValues.length;
			}
		}

		return aggregatedMetrics;
	}
}
