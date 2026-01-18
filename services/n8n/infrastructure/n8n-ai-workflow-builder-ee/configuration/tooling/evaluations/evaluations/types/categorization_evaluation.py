"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/evaluations/types/categorization-evaluation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/evaluations/types 的工作流类型。导入/依赖:外部:zod；内部:无；本地:../types/categorization。导出:categorizationTestCaseSchema、CategorizationTestCase、CategorizationTestResult、TechniqueFrequency、CategorizationEvaluationSummary、CategorizationEvaluationOutput。关键函数/方法:无。用于定义工作流相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI builder evaluation harness/scripts -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/evaluations/types/categorization-evaluation.ts -> services/n8n/infrastructure/n8n-ai-workflow-builder-ee/configuration/tooling/evaluations/evaluations/types/categorization_evaluation.py

import { z } from 'zod';

import type { PromptCategorization, WorkflowTechniqueType } from '../../src/types/categorization';

/**
 * Test case for categorization evaluation
 */
export const categorizationTestCaseSchema = z.object({
	id: z.string(),
	prompt: z.string(),
});

export type CategorizationTestCase = z.infer<typeof categorizationTestCaseSchema>;

/**
 * Result of a single categorization test
 */
export interface CategorizationTestResult {
	testCase: CategorizationTestCase;
	categorization: PromptCategorization;
	techniqueDescriptions: Record<WorkflowTechniqueType, string>;
	executionTime: number;
	error?: string;
}

/**
 * Technique frequency statistics
 */
export interface TechniqueFrequency {
	technique: WorkflowTechniqueType;
	description: string;
	count: number;
	percentage: number;
}

/**
 * Summary of categorization evaluation results
 */
export interface CategorizationEvaluationSummary {
	totalPrompts: number;
	successfulCategorizations: number;
	failedCategorizations: number;
	averageConfidence: number;
	averageExecutionTime: number;
	techniqueFrequencies: TechniqueFrequency[];
}

/**
 * Complete categorization evaluation output
 */
export interface CategorizationEvaluationOutput {
	timestamp: string;
	summary: CategorizationEvaluationSummary;
	results: CategorizationTestResult[];
}
