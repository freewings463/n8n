"""
MIGRATION-META:
  source_path: packages/cli/src/controllers/workflow-statistics.types.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/controllers 的工作流控制器。导入/依赖:外部:无；内部:@/executions/execution.types；本地:无。导出:GetOne。关键函数/方法:无。用于处理工作流接口请求，调度服务/仓储并返回响应。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Controller -> presentation/api/v1/controllers
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/controllers/workflow-statistics.types.ts -> services/n8n/presentation/cli/api/v1/controllers/workflow_statistics_types.py

import type { ExecutionRequest } from '@/executions/execution.types';

export namespace StatisticsRequest {
	export type GetOne = ExecutionRequest.GetOne;
}
