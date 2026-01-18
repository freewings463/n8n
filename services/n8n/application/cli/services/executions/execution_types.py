"""
MIGRATION-META:
  source_path: packages/cli/src/executions/execution.types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/executions 的执行类型。导入/依赖:外部:无；内部:@n8n/db；本地:无。导出:StopResult。关键函数/方法:无。用于定义执行相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Execution read/write helpers -> application/services/executions
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/executions/execution.types.ts -> services/n8n/application/cli/services/executions/execution_types.py

import type { AuthenticatedRequest, ExecutionSummaries, ExecutionEntity } from '@n8n/db';
import type {
	AnnotationVote,
	ExecutionStatus,
	IDataObject,
	WorkflowExecuteMode,
} from 'n8n-workflow';

export declare namespace ExecutionRequest {
	namespace QueryParams {
		type GetMany = {
			filter: string; // stringified `FilterFields`
			limit: string;
			lastId: string;
			firstId: string;
		};
	}

	namespace BodyParams {
		type DeleteFilter = {
			deleteBefore?: Date;
			filters?: IDataObject;
			ids?: string[];
		};

		type StopMany = {
			filter: ExecutionSummaries.StopExecutionFilterQuery; // stringified `FilterFields`
		};
	}

	namespace RouteParams {
		type ExecutionId = {
			id: ExecutionEntity['id'];
		};
	}

	type ExecutionUpdatePayload = {
		tags?: string[];
		vote?: AnnotationVote | null;
	};

	type GetMany = AuthenticatedRequest<{}, {}, {}, QueryParams.GetMany> & {
		rangeQuery: ExecutionSummaries.RangeQuery; // parsed from query params
	};

	type GetOne = AuthenticatedRequest<RouteParams.ExecutionId>;

	type Delete = AuthenticatedRequest<{}, {}, BodyParams.DeleteFilter>;

	type Retry = AuthenticatedRequest<RouteParams.ExecutionId, {}, { loadWorkflow?: boolean }, {}>;

	type Stop = AuthenticatedRequest<RouteParams.ExecutionId>;
	type StopMany = AuthenticatedRequest<{}, {}, BodyParams.StopMany>;

	type Update = AuthenticatedRequest<RouteParams.ExecutionId, {}, ExecutionUpdatePayload, {}>;
}

export type StopResult = {
	mode: WorkflowExecuteMode;
	startedAt: Date;
	stoppedAt?: Date;
	finished: boolean;
	status: ExecutionStatus;
};
