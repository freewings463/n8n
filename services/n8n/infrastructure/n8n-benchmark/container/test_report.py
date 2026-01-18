"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/src/test-execution/test-report.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/src/test-execution 的执行模块。导入/依赖:外部:nanoid；内部:@/test-execution/prometheus-metrics-parser、@/types/scenario；本地:无。导出:K6Tag、Check、CounterMetric、TrendMetric、AppMetricStats、AppMetricsReport、TestReport、buildAppMetricsReport 等1项。关键函数/方法:k6CheckToCheck、k6CounterToCounter、k6TrendToTrend、buildAppMetricsReport、buildTestReport。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark test execution (k6/process/metrics) -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/src/test-execution/test-report.ts -> services/n8n/infrastructure/n8n-benchmark/container/test_report.py

import { nanoid } from 'nanoid';

import { PrometheusMetricsParser } from '@/test-execution/prometheus-metrics-parser';
import type { Scenario } from '@/types/scenario';

export type K6Tag = {
	name: string;
	value: string;
};

export type Check = {
	name: string;
	passes: number;
	fails: number;
};

export type CounterMetric = {
	type: 'counter';
	count: number;
	rate: number;
};

export type TrendMetric = {
	type: 'trend';
	'p(95)': number;
	avg: number;
	min: number;
	med: number;
	max: number;
	'p(90)': number;
};

export type AppMetricStats = {
	max: number;
	avg: number;
	min: number;
	count: number;
};

export type AppMetricsReport = {
	heapSizeTotal?: AppMetricStats;
	heapSizeUsed?: AppMetricStats;
	externalMemory?: AppMetricStats;
	eventLoopLag?: AppMetricStats;
};

export type TestReport = {
	runId: string;
	ts: string; // ISO8601
	scenarioName: string;
	tags: K6Tag[];
	metrics: {
		iterations: CounterMetric;
		dataReceived: CounterMetric;
		dataSent: CounterMetric;
		httpRequests: CounterMetric;
		httpRequestDuration: TrendMetric;
		httpRequestSending: TrendMetric;
		httpRequestReceiving: TrendMetric;
		httpRequestWaiting: TrendMetric;
	};
	checks: Check[];
	appMetrics?: AppMetricsReport;
};

function k6CheckToCheck(check: K6Check): Check {
	return {
		name: check.name,
		passes: check.passes,
		fails: check.fails,
	};
}

function k6CounterToCounter(counter: K6CounterMetric): CounterMetric {
	return {
		type: 'counter',
		count: counter.values.count,
		rate: counter.values.rate,
	};
}

function k6TrendToTrend(trend: K6TrendMetric): TrendMetric {
	return {
		type: 'trend',
		'p(90)': trend.values['p(90)'],
		avg: trend.values.avg,
		min: trend.values.min,
		med: trend.values.med,
		max: trend.values.max,
		'p(95)': trend.values['p(95)'],
	};
}

/**
 * Builds an app metrics report from collected Prometheus metrics data
 */
export function buildAppMetricsReport(metricsData: string[]): AppMetricsReport {
	const heapSizeTotal = PrometheusMetricsParser.calculateMetricStats(
		metricsData,
		'n8n_nodejs_heap_size_total_bytes',
	);
	const heapSizeUsed = PrometheusMetricsParser.calculateMetricStats(
		metricsData,
		'n8n_nodejs_heap_size_used_bytes',
	);
	const externalMemory = PrometheusMetricsParser.calculateMetricStats(
		metricsData,
		'n8n_nodejs_external_memory_bytes',
	);
	const eventLoopLag = PrometheusMetricsParser.calculateMetricStats(
		metricsData,
		'n8n_nodejs_eventloop_lag_seconds',
	);

	return {
		...(heapSizeTotal && { heapSizeTotal }),
		...(heapSizeUsed && { heapSizeUsed }),
		...(externalMemory && { externalMemory }),
		...(eventLoopLag && { eventLoopLag }),
	};
}

/**
 * Converts the k6 test summary to a test report
 */
export function buildTestReport(
	scenario: Scenario,
	endOfTestSummary: K6EndOfTestSummary,
	tags: K6Tag[],
	appMetricsData?: string[],
): TestReport {
	const appMetrics = appMetricsData ? buildAppMetricsReport(appMetricsData) : undefined;

	return {
		runId: nanoid(),
		ts: new Date().toISOString(),
		scenarioName: scenario.name,
		tags,
		checks: endOfTestSummary.root_group.checks.map(k6CheckToCheck),
		metrics: {
			dataReceived: k6CounterToCounter(endOfTestSummary.metrics.data_received),
			dataSent: k6CounterToCounter(endOfTestSummary.metrics.data_sent),
			httpRequests: k6CounterToCounter(endOfTestSummary.metrics.http_reqs),
			httpRequestDuration: k6TrendToTrend(endOfTestSummary.metrics.http_req_duration),
			httpRequestSending: k6TrendToTrend(endOfTestSummary.metrics.http_req_sending),
			httpRequestReceiving: k6TrendToTrend(endOfTestSummary.metrics.http_req_receiving),
			httpRequestWaiting: k6TrendToTrend(endOfTestSummary.metrics.http_req_waiting),
			iterations: k6CounterToCounter(endOfTestSummary.metrics.iterations),
		},
		...(appMetrics && { appMetrics }),
	};
}
