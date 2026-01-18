"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/ai/ai-build-request.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/ai 的模块。导入/依赖:外部:zod、zod-class；内部:n8n-workflow；本地:无。导出:ExpressionValue、AiBuilderChatRequestDto。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/ai/ai-build-request.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/ai/ai_build_request_dto.py

import type { IRunExecutionData, IWorkflowBase, NodeExecutionSchema } from 'n8n-workflow';
import { z } from 'zod';
import { Z } from 'zod-class';

export interface ExpressionValue {
	expression: string;
	resolvedValue: unknown;
	nodeType?: string;
}

export class AiBuilderChatRequestDto extends Z.class({
	payload: z.object({
		id: z.string(),
		role: z.literal('user'),
		type: z.literal('message'),
		text: z.string(),
		versionId: z.string().optional(),
		workflowContext: z.object({
			currentWorkflow: z
				.custom<Partial<IWorkflowBase>>((val: Partial<IWorkflowBase>) => {
					if (!val.nodes && !val.connections) {
						return false;
					}

					return val;
				})
				.optional(),

			executionData: z
				.custom<IRunExecutionData['resultData']>((val: IRunExecutionData['resultData']) => {
					if (!val.runData && !val.error) {
						return false;
					}

					return val;
				})
				.optional(),

			executionSchema: z
				.custom<NodeExecutionSchema[]>((val: NodeExecutionSchema[]) => {
					// Check if the array is empty or if all items have nodeName and schema properties
					if (!Array.isArray(val) || val.every((item) => !item.nodeName || !item.schema)) {
						return false;
					}

					return val;
				})
				.optional(),

			expressionValues: z
				.custom<Record<string, ExpressionValue[]>>((val: Record<string, ExpressionValue[]>) => {
					const keys = Object.keys(val);
					// Check if the array is empty or if all items have nodeName and schema properties
					if (keys.length > 0 && keys.every((key) => val[key].every((v) => !v.expression))) {
						return false;
					}

					return val;
				})
				.optional(),
		}),
		featureFlags: z
			.object({
				templateExamples: z.boolean().optional(),
				multiAgent: z.boolean().optional(),
			})
			.optional(),
	}),
}) {}
