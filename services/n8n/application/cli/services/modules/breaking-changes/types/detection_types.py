"""
MIGRATION-META:
  source_path: packages/cli/src/modules/breaking-changes/types/detection.types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/breaking-changes/types 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:WorkflowDetectionReport、InstanceDetectionReport、BatchWorkflowDetectionReport。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/breaking-changes/types/detection.types.ts -> services/n8n/application/cli/services/modules/breaking-changes/types/detection_types.py

import type {
	BreakingChangeInstanceIssue,
	BreakingChangeRecommendation,
	BreakingChangeWorkflowIssue,
} from '@n8n/api-types';

export interface WorkflowDetectionReport {
	isAffected: boolean;
	issues: BreakingChangeWorkflowIssue[]; // List of issues affecting this workflow
}

export interface InstanceDetectionReport {
	isAffected: boolean;
	instanceIssues: BreakingChangeInstanceIssue[];
	recommendations: BreakingChangeRecommendation[];
}

/**
 * Report returned by batch workflow rules after processing all workflows.
 * Used when a rule needs to correlate data across multiple workflows before producing results.
 */
export interface BatchWorkflowDetectionReport {
	affectedWorkflows: Array<{
		workflowId: string;
		issues: BreakingChangeWorkflowIssue[];
	}>;
}
