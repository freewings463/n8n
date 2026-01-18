"""
MIGRATION-META:
  source_path: packages/cli/src/executions/validation.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/executions 的执行模块。导入/依赖:外部:zod；内部:@/errors/…/bad-request.error、@/executions/execution.types；本地:无。导出:validateExecutionUpdatePayload。关键函数/方法:validateExecutionUpdatePayload。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Execution read/write helpers -> application/services/executions
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/executions/validation.ts -> services/n8n/application/cli/services/executions/validation.py

import { z } from 'zod';

import { BadRequestError } from '@/errors/response-errors/bad-request.error';
import type { ExecutionRequest } from '@/executions/execution.types';

const executionUpdateSchema = z.object({
	tags: z.array(z.string()).optional(),
	vote: z.enum(['up', 'down']).nullable().optional(),
});

export function validateExecutionUpdatePayload(
	payload: unknown,
): ExecutionRequest.ExecutionUpdatePayload {
	try {
		const validatedPayload = executionUpdateSchema.parse(payload);

		// Additional check to ensure that at least one property is provided
		const { tags, vote } = validatedPayload;
		if (!tags && vote === undefined) {
			throw new BadRequestError('No annotation provided');
		}

		return validatedPayload;
	} catch (e) {
		if (e instanceof z.ZodError) {
			throw new BadRequestError(e.message);
		}

		throw e;
	}
}
