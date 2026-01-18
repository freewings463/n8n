"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/schemas/workflow-execution-status.schema.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/schemas 的工作流模块。导入/依赖:外部:zod；内部:无；本地:无。导出:WorkflowExecutionStatusSchema、WorkflowExecutionStatus。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/schemas/workflow-execution-status.schema.ts -> services/n8n/presentation/n8n-api-types/dto/schemas/workflow_execution_status_schema.py

import { z } from 'zod';

export const WorkflowExecutionStatusSchema = z.object({
	workflowId: z.string(),
	credentials: z
		.array(
			z.object({
				credentialId: z.string(),
				credentialName: z.string(),
				credentialType: z.string(),
				credentialStatus: z.enum(['missing', 'configured']),
				authorizationUrl: z.string().optional(),
			}),
		)
		.optional(),
	readyToExecute: z.boolean(),
});

export type WorkflowExecutionStatus = z.infer<typeof WorkflowExecutionStatusSchema>;
