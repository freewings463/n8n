"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/schemas/project.schema.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/schemas 的模块。导入/依赖:外部:zod；内部:@n8n/permissions；本地:无。导出:projectNameSchema、projectTypeSchema、ProjectType、projectIconSchema、ProjectIcon、projectDescriptionSchema、projectRelationSchema、ProjectRelation。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/schemas/project.schema.ts -> services/n8n/presentation/n8n-api-types/dto/schemas/project_schema.py

import { assignableProjectRoleSchema } from '@n8n/permissions';
import { z } from 'zod';

export const projectNameSchema = z.string().min(1).max(255);

export const projectTypeSchema = z.enum(['personal', 'team']);
export type ProjectType = z.infer<typeof projectTypeSchema>;

export const projectIconSchema = z.object({
	type: z.enum(['emoji', 'icon']),
	value: z.string().min(1),
});
export type ProjectIcon = z.infer<typeof projectIconSchema>;

export const projectDescriptionSchema = z.string().max(512);

export const projectRelationSchema = z.object({
	userId: z.string().min(1),
	role: assignableProjectRoleSchema,
});
export type ProjectRelation = z.infer<typeof projectRelationSchema>;
