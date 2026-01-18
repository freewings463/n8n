"""
MIGRATION-META:
  source_path: packages/cli/src/modules/breaking-changes/types/rule.types.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/breaking-changes/types 的类型。导入/依赖:外部:无；内部:@n8n/db、n8n-workflow；本地:无。导出:enum、BreakingChangeRuleMetadata、IBreakingChangeInstanceRule、IBreakingChangeWorkflowRule、IBreakingChangeBatchWorkflowRule、IBreakingChangeRule。关键函数/方法:getMetadata、detect、getRecommendations、detectWorkflow、collectWorkflowData、produceReport、reset。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/breaking-changes/types/rule.types.ts -> services/n8n/application/cli/services/modules/breaking-changes/types/rule_types.py

import type {
	BreakingChangeAffectedWorkflow,
	BreakingChangeRecommendation,
	BreakingChangeRuleSeverity,
	BreakingChangeVersion,
} from '@n8n/api-types';
import type { WorkflowEntity } from '@n8n/db';
import type { INode } from 'n8n-workflow';

import type {
	BatchWorkflowDetectionReport,
	InstanceDetectionReport,
	WorkflowDetectionReport,
} from './detection.types';

export const enum BreakingChangeCategory {
	workflow = 'workflow',
	instance = 'instance',
	environment = 'environment',
	database = 'database',
	infrastructure = 'infrastructure',
}

export interface BreakingChangeRuleMetadata {
	version: BreakingChangeVersion;
	title: string;
	description: string;
	category: BreakingChangeCategory;
	severity: BreakingChangeRuleSeverity;
	documentationUrl?: string;
}

export interface IBreakingChangeInstanceRule {
	id: string;
	getMetadata(): BreakingChangeRuleMetadata;
	detect(): Promise<InstanceDetectionReport>;
}

export interface IBreakingChangeWorkflowRule {
	id: string;
	getMetadata(): BreakingChangeRuleMetadata;
	getRecommendations(
		workflowResults: BreakingChangeAffectedWorkflow[],
	): Promise<BreakingChangeRecommendation[]>;
	// The detectWorkflow function includes the nodes grouped by type for more efficient processing
	detectWorkflow(
		workflow: WorkflowEntity,
		nodesGroupedByType: Map<string, INode[]>,
	): Promise<WorkflowDetectionReport>;
}

/**
 * Interface for batch-based workflow rules that need to correlate data across multiple workflows.
 * Unlike IBreakingChangeWorkflowRule which processes each workflow independently,
 * batch rules collect data from all workflows first, then produce a final report.
 *
 * Use case example: Detecting parent workflows that call sub-workflows with specific characteristics,
 * where the rule needs to identify both the sub-workflows and their callers before reporting.
 */
export interface IBreakingChangeBatchWorkflowRule {
	id: string;
	getMetadata(): BreakingChangeRuleMetadata;
	getRecommendations(
		workflowResults: BreakingChangeAffectedWorkflow[],
	): Promise<BreakingChangeRecommendation[]>;

	/**
	 * Called for each workflow during the scanning phase.
	 * The rule should collect and store any relevant data internally.
	 */
	collectWorkflowData(
		workflow: WorkflowEntity,
		nodesGroupedByType: Map<string, INode[]>,
	): Promise<void>;

	/**
	 * Called after all workflows have been scanned to produce the final report.
	 * The rule should correlate the collected data and return the affected workflows.
	 */
	produceReport(): Promise<BatchWorkflowDetectionReport>;

	/**
	 * Called to reset internal state before a new detection run.
	 */
	reset(): void;
}

export type IBreakingChangeRule =
	| IBreakingChangeInstanceRule
	| IBreakingChangeWorkflowRule
	| IBreakingChangeBatchWorkflowRule;
