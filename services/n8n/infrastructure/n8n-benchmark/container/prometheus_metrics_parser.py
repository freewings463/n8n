"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/src/test-execution/prometheus-metrics-parser.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/src/test-execution 的执行模块。导入/依赖:外部:无；内部:无；本地:无。导出:PrometheusMetricsParser。关键函数/方法:extractMetricValues、calculateMetricStats。用于承载执行实现细节，并通过导出对外提供能力。注释目标:Parses Prometheus metrics text format and extracts time series data。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark test execution (k6/process/metrics) -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/src/test-execution/prometheus-metrics-parser.ts -> services/n8n/infrastructure/n8n-benchmark/container/prometheus_metrics_parser.py

/**
 * Parses Prometheus metrics text format and extracts time series data
 */
export class PrometheusMetricsParser {
	/**
	 * Extracts all values for a specific metric from collected metrics data
	 */
	static extractMetricValues(metricsData: string[], metricName: string): number[] {
		const values: number[] = [];

		for (const metricsText of metricsData) {
			const lines = metricsText.split('\n');

			for (const line of lines) {
				// Skip comments and empty lines
				if (line.startsWith('#') || line.trim() === '') {
					continue;
				}

				// Parse metric line: metric_name{labels} value
				// For example: n8n_nodejs_heap_size_total_bytes 149159936
				// For simplicity, we'll just check if the line starts with the metric name
				if (line.startsWith(metricName)) {
					const parts = line.split(/\s+/);
					if (parts.length >= 2) {
						const value = parseFloat(parts[parts.length - 1]);
						if (!isNaN(value)) {
							values.push(value);
						}
					}
				}
			}
		}

		return values;
	}

	/**
	 * Calculates statistics for a metric from collected data
	 */
	static calculateMetricStats(
		metricsData: string[],
		metricName: string,
	): { max: number; avg: number; min: number; count: number } | null {
		const values = this.extractMetricValues(metricsData, metricName);

		if (values.length === 0) {
			return null;
		}

		const max = Math.max(...values);
		const min = Math.min(...values);
		const sum = values.reduce((a, b) => a + b, 0);
		const avg = sum / values.length;

		return {
			max,
			min,
			avg,
			count: values.length,
		};
	}
}
