"""
MIGRATION-META:
  source_path: packages/cli/src/modules/mcp/tools/schemas.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/mcp/tools 的模块。导入/依赖:外部:zod；内部:n8n-workflow；本地:无。导出:nodeSchema、tagSchema、workflowSettingsSchema、workflowMetaSchema、workflowDetailsOutputSchema。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/mcp/tools/schemas.ts -> services/n8n/tests/cli/unit/modules/mcp/tools/schemas.py

import type { IWorkflowSettings, WorkflowFEMeta } from 'n8n-workflow';
import z from 'zod';

export const nodeSchema = z
	.object({
		name: z.string(),
		type: z.string(),
	})
	.passthrough();

export const tagSchema = z.object({ id: z.string(), name: z.string() }).passthrough();

export const workflowSettingsSchema = z
	.custom<IWorkflowSettings>((_value): _value is IWorkflowSettings => true)
	.nullable();

export const workflowMetaSchema = z
	.custom<WorkflowFEMeta>((_value): _value is WorkflowFEMeta => true)
	.nullable();

export const workflowDetailsOutputSchema = z.object({
	workflow: z
		.object({
			id: z.string(),
			name: z.string().nullable(),
			active: z.boolean(),
			isArchived: z.boolean(),
			versionId: z.string(),
			triggerCount: z.number(),
			createdAt: z.string().nullable(),
			updatedAt: z.string().nullable(),
			settings: workflowSettingsSchema,
			connections: z.record(z.unknown()),
			nodes: z.array(nodeSchema),
			tags: z.array(tagSchema),
			meta: workflowMetaSchema,
			parentFolderId: z.string().nullable(),
			description: z.string().optional().describe('The description of the workflow'),
		})
		.passthrough()
		.describe('Sanitized workflow data safe for MCP consumption'),
	triggerInfo: z
		.string()
		.describe('Human-readable instructions describing how to trigger the workflow'),
});
