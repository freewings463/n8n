"""
MIGRATION-META:
  source_path: packages/cli/src/metrics/types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/metrics 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:MetricCategory、MetricLabel、Includes。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/metrics/types.ts -> services/n8n/application/cli/services/metrics/types.py

export type MetricCategory =
	| 'default'
	| 'routes'
	| 'cache'
	| 'logs'
	| 'queue'
	| 'workflowStatistics';

export type MetricLabel =
	| 'credentialsType'
	| 'nodeType'
	| 'workflowId'
	| 'workflowName'
	| 'apiPath'
	| 'apiMethod'
	| 'apiStatusCode';

export type Includes = {
	metrics: Record<MetricCategory, boolean>;
	labels: Record<MetricLabel, boolean>;
};
