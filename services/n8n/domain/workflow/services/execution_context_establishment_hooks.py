"""
MIGRATION-META:
  source_path: packages/workflow/src/execution-context-establishment-hooks.ts
  target_context: n8n
  target_layer: Domain
  responsibility: 位于 packages/workflow/src 的工作流模块。导入/依赖:外部:zod/v4；内部:无；本地:无。导出:ExecutionContextEstablishmentHookParameterV1、ExecutionContextEstablishmentHookParameterSchema、ExecutionContextEstablishmentHookParameter、toExecutionContextEstablishmentHookParameter。关键函数/方法:toExecutionContextEstablishmentHookParameter。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow treated as domain model & rules
    - Rewrite implementation for Domain layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/src/execution-context-establishment-hooks.ts -> services/n8n/domain/workflow/services/execution_context_establishment_hooks.py

import z from 'zod/v4';

const ExecutionContextEstablishmentHookParameterSchemaV1 = z.object({
	executionsHooksVersion: z.literal(1),
	contextEstablishmentHooks: z.object({
		hooks: z.array(
			z
				.object({
					hookName: z.string(),
					isAllowedToFail: z.boolean().optional().default(false),
				})
				.loose(),
		),
	}),
});

export type ExecutionContextEstablishmentHookParameterV1 = z.output<
	typeof ExecutionContextEstablishmentHookParameterSchemaV1
>;

export const ExecutionContextEstablishmentHookParameterSchema = z
	.discriminatedUnion('executionsHooksVersion', [
		ExecutionContextEstablishmentHookParameterSchemaV1,
	])
	.meta({
		title: 'ExecutionContextEstablishmentHookParameter',
	});

export type ExecutionContextEstablishmentHookParameter = z.output<
	typeof ExecutionContextEstablishmentHookParameterSchema
>;

/**
 * Safely parses an execution context establishment hook parameters
 * @param obj
 * @returns
 */
export const toExecutionContextEstablishmentHookParameter = (value: unknown) => {
	if (value === null || value === undefined || typeof value !== 'object') {
		return null;
	}
	// Quick check to avoid unnecessary parsing attempts
	if (!('executionsHooksVersion' in value)) {
		return null;
	}
	return ExecutionContextEstablishmentHookParameterSchema.safeParse(value);
};
