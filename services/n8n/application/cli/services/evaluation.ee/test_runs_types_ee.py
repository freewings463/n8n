"""
MIGRATION-META:
  source_path: packages/cli/src/evaluation.ee/test-runs.types.ee.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/evaluation.ee 的类型。导入/依赖:外部:无；内部:@n8n/db、@/requests；本地:无。导出:无。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/evaluation.ee/test-runs.types.ee.ts -> services/n8n/application/cli/services/evaluation.ee/test_runs_types_ee.py

import type { AuthenticatedRequest } from '@n8n/db';

import type { ListQuery } from '@/requests';

export declare namespace TestRunsRequest {
	namespace RouteParams {
		type WorkflowId = {
			workflowId: string;
		};

		type TestRunId = {
			id: string;
		};
	}

	type Create = AuthenticatedRequest<RouteParams.WorkflowId>;

	type GetMany = AuthenticatedRequest<RouteParams.WorkflowId, {}, {}, ListQuery.Params> & {
		listQueryOptions: ListQuery.Options;
	};

	type GetOne = AuthenticatedRequest<RouteParams.WorkflowId & RouteParams.TestRunId>;

	type Delete = AuthenticatedRequest<RouteParams.WorkflowId & RouteParams.TestRunId>;

	type Cancel = AuthenticatedRequest<RouteParams.WorkflowId & RouteParams.TestRunId>;

	type GetCases = AuthenticatedRequest<RouteParams.WorkflowId & RouteParams.TestRunId>;
}
