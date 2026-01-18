"""
MIGRATION-META:
  source_path: packages/cli/src/events/maps/queue-metrics.event-map.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/events/maps 的队列模块。导入/依赖:外部:无；内部:无；本地:无。导出:QueueMetricsEventMap。关键函数/方法:无。用于承载队列实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/events/maps/queue-metrics.event-map.ts -> services/n8n/application/cli/services/events/maps/queue_metrics_event_map.py

export type QueueMetricsEventMap = {
	'job-counts-updated': {
		active: number;
		completed: number;
		failed: number;
		waiting: number;
	};
};
