"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/src/test-execution/app-metrics-poller.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/src/test-execution 的执行模块。导入/依赖:外部:无；内部:无；本地:无。导出:AppMetricsPoller。关键函数/方法:start、stop、clearInterval、getMetricsData、pollMetrics。用于承载执行实现细节，并通过导出对外提供能力。注释目标:Polls the /metrics endpoint from an n8n instance to collect application metrics / during benchmark test runs.。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected external HTTP client usage -> infrastructure/external_services/clients
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/src/test-execution/app-metrics-poller.ts -> services/n8n/infrastructure/n8n-benchmark/external_services/clients/test-execution/app_metrics_poller.py

/**
 * Polls the /metrics endpoint from an n8n instance to collect application metrics
 * during benchmark test runs.
 *
 * A Poller can be started and stopped once. After it's stopped, it cannot be restarted.
 * Instead, a new poller instance should be created.
 */
export class AppMetricsPoller {
	private intervalId: NodeJS.Timeout | undefined = undefined;
	private metricsData: string[] = [];
	private isRunning = false;
	private isStopped = false;

	constructor(
		private readonly metricsUrl: string,
		private readonly pollIntervalMs: number = 5000,
	) {}

	/**
	 * Starts polling the metrics endpoint
	 */
	start() {
		if (this.isRunning) {
			throw new Error('Metrics poller is already running');
		}
		if (this.isStopped) {
			throw new Error('Metrics poller has been stopped and cannot be restarted');
		}

		this.isRunning = true;
		this.metricsData = [];

		// Immediately poll once to get initial metrics
		void this.pollMetrics();

		// Set up interval polling
		this.intervalId = setInterval(() => {
			void this.pollMetrics();
		}, this.pollIntervalMs);
	}

	/**
	 * Stops polling the metrics endpoint
	 */
	stop() {
		if (this.intervalId) {
			clearInterval(this.intervalId);
			this.intervalId = undefined;
		}
		this.isRunning = false;
		this.isStopped = true;
	}

	/**
	 * Gets all collected metrics data
	 */
	getMetricsData(): string[] {
		return this.metricsData;
	}

	/**
	 * Polls the metrics endpoint once
	 */
	private async pollMetrics() {
		try {
			const response = await fetch(this.metricsUrl);

			if (!response.ok) {
				console.warn(`Failed to poll metrics: ${response.status} ${response.statusText}`);
				return;
			}

			const metricsText = await response.text();
			this.metricsData.push(metricsText);
		} catch (error) {
			console.warn(
				`Error polling metrics: ${error instanceof Error ? error.message : String(error)}`,
			);
		}
	}
}
