"""
MIGRATION-META:
  source_path: packages/testing/containers/services/observability.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/containers/services 的服务。导入/依赖:外部:无；内部:无；本地:./types 等2项。导出:escapeLogsQL、LogsHelper、type LogEntry、type LogQueryOptions、ObservabilityHelper、createObservabilityHelper。关键函数/方法:createObservabilityHelper。用于封装该模块业务流程，对上提供稳定调用面。注释目标:Combined observability helper that provides unified access to logs and metrics. / The actual services are in victoria-logs.ts and victoria-metrics.ts.。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (containers harness) -> tests/fixtures/containers
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/containers/services/observability.ts -> services/n8n/tests/testing/fixtures/containers/services/observability.py

/**
 * Combined observability helper that provides unified access to logs and metrics.
 * The actual services are in victoria-logs.ts and victoria-metrics.ts.
 */
import type { HelperContext } from './types';
import { LogsHelper, type VictoriaLogsResult, escapeLogsQL } from './victoria-logs';
import { MetricsHelper, type VictoriaMetricsResult } from './victoria-metrics';

export { escapeLogsQL };
export { LogsHelper, type LogEntry, type LogQueryOptions } from './victoria-logs';
export {
	MetricsHelper,
	type MetricResult,
	type WaitForMetricOptions,
	type ScrapeTarget,
} from './victoria-metrics';

export class ObservabilityHelper {
	readonly logs: LogsHelper;
	readonly metrics: MetricsHelper;
	readonly syslog: VictoriaLogsResult['meta']['syslog'];

	constructor(logsMeta: VictoriaLogsResult['meta'], metricsMeta: VictoriaMetricsResult['meta']) {
		this.logs = new LogsHelper(logsMeta.queryEndpoint);
		this.metrics = new MetricsHelper(metricsMeta.queryEndpoint);
		this.syslog = logsMeta.syslog;
	}
}

export function createObservabilityHelper(ctx: HelperContext): ObservabilityHelper {
	const logsResult = ctx.serviceResults.victoriaLogs as VictoriaLogsResult | undefined;
	const metricsResult = ctx.serviceResults.victoriaMetrics as VictoriaMetricsResult | undefined;

	if (!logsResult) {
		throw new Error('VictoriaLogs service not found in context');
	}
	if (!metricsResult) {
		throw new Error('VictoriaMetrics service not found in context');
	}

	return new ObservabilityHelper(logsResult.meta, metricsResult.meta);
}

declare module './types' {
	interface ServiceHelpers {
		observability: ObservabilityHelper;
	}
}
