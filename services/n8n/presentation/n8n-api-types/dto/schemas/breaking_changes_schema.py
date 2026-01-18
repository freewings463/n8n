"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/schemas/breaking-changes.schema.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/schemas 的模块。导入/依赖:外部:zod；内部:无；本地:无。导出:breakingChangeRuleSeveritySchema、BreakingChangeRuleSeverity、breakingChangeIssueLevelSchema、BreakingChangeVersion、BreakingChangeRecommendation、BreakingChangeInstanceIssue、BreakingChangeWorkflowIssue、BreakingChangeAffectedWorkflow 等4项。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/schemas/breaking-changes.schema.ts -> services/n8n/presentation/n8n-api-types/dto/schemas/breaking_changes_schema.py

import { z } from 'zod';

// Enums
export const breakingChangeRuleSeveritySchema = z.enum(['low', 'medium', 'critical']);
export type BreakingChangeRuleSeverity = z.infer<typeof breakingChangeRuleSeveritySchema>;

export const breakingChangeIssueLevelSchema = z.enum(['info', 'warning', 'error']);

const breakingChangeVersionSchema = z.enum(['v2']);
export type BreakingChangeVersion = z.infer<typeof breakingChangeVersionSchema>;

// Common schemas
const recommendationSchema = z.object({
	action: z.string(),
	description: z.string(),
});
export type BreakingChangeRecommendation = z.infer<typeof recommendationSchema>;

const instanceIssueSchema = z.object({
	title: z.string(),
	description: z.string(),
	level: breakingChangeIssueLevelSchema,
});
export type BreakingChangeInstanceIssue = z.infer<typeof instanceIssueSchema>;

const workflowIssueSchema = instanceIssueSchema.extend({
	nodeId: z.string().optional(),
	nodeName: z.string().optional(),
});
export type BreakingChangeWorkflowIssue = z.infer<typeof workflowIssueSchema>;

const affectedWorkflowSchema = z.object({
	id: z.string(),
	name: z.string(),
	active: z.boolean(),
	numberOfExecutions: z.number(),
	lastUpdatedAt: z.date(),
	lastExecutedAt: z.date().optional(),
	issues: z.array(workflowIssueSchema),
});
export type BreakingChangeAffectedWorkflow = z.infer<typeof affectedWorkflowSchema>;

const ruleResultBaseSchema = z.object({
	ruleId: z.string(),
	ruleTitle: z.string(),
	ruleDescription: z.string(),
	ruleSeverity: breakingChangeRuleSeveritySchema,
	ruleDocumentationUrl: z.string().optional(),
	recommendations: z.array(recommendationSchema),
});

const instanceRuleResultsSchema = ruleResultBaseSchema.extend({
	instanceIssues: z.array(instanceIssueSchema),
});
export type BreakingChangeInstanceRuleResult = z.infer<typeof instanceRuleResultsSchema>;

const workflowRuleResultsSchema = ruleResultBaseSchema.extend({
	affectedWorkflows: z.array(affectedWorkflowSchema),
});
export type BreakingChangeWorkflowRuleResult = z.infer<typeof workflowRuleResultsSchema>;

const breakingChangeReportDataSchema = {
	generatedAt: z.date(),
	targetVersion: z.string(),
	currentVersion: z.string(),
	instanceResults: z.array(instanceRuleResultsSchema),
	workflowResults: z.array(workflowRuleResultsSchema),
} as const;

const breakingChangeReportSchema = z.object(breakingChangeReportDataSchema).strict();

const breakingChangeLightReportDataSchema = {
	generatedAt: z.date(),
	targetVersion: z.string(),
	currentVersion: z.string(),
	instanceResults: z.array(instanceRuleResultsSchema),
	workflowResults: z.array(
		workflowRuleResultsSchema.omit({ affectedWorkflows: true }).extend({
			nbAffectedWorkflows: z.number(),
		}),
	),
} as const;

const breakingChangeLightReportSchema = z.object(breakingChangeLightReportDataSchema).strict();

const breakingChangeReportResultDataSchema = z.object({
	report: breakingChangeReportSchema,
	totalWorkflows: z.number(),
	shouldCache: z.boolean(),
});
export type BreakingChangeReportResult = z.infer<typeof breakingChangeReportResultDataSchema>;

const breakingChangeLightReportResultDataSchema = z.object({
	report: breakingChangeLightReportSchema,
	totalWorkflows: z.number(),
	shouldCache: z.boolean(),
});
export type BreakingChangeLightReportResult = z.infer<
	typeof breakingChangeLightReportResultDataSchema
>;
