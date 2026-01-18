"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/schemas/usage.schema.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/schemas 的模块。导入/依赖:外部:zod；内部:无；本地:无。导出:usageStateSchema、UsageState。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/schemas/usage.schema.ts -> services/n8n/presentation/n8n-api-types/dto/schemas/usage_schema.py

import { z } from 'zod';

export const usageStateSchema = z.object({
	loading: z.boolean(),
	data: z.object({
		usage: z.object({
			activeWorkflowTriggers: z.object({
				limit: z.number(), // -1 for unlimited, from license
				value: z.number(),
				warningThreshold: z.number(),
			}),
			workflowsHavingEvaluations: z.object({
				limit: z.number(), // -1 for unlimited, from license
				value: z.number(),
			}),
		}),
		license: z.object({
			planId: z.string(), // community
			planName: z.string(), // defaults to Community
		}),
		managementToken: z.string().optional(),
	}),
});

export type UsageState = z.infer<typeof usageStateSchema>;
