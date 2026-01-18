"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/schemas/source-controlled-file.schema.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/schemas 的模块。导入/依赖:外部:zod；内部:无；本地:无。导出:SOURCE_CONTROL_FILE_TYPE、SOURCE_CONTROL_FILE_STATUS、SourceControlledFileStatus、isSourceControlledFileStatus、SOURCE_CONTROL_FILE_LOCATION、SourceControlledFileSchema、SourceControlledFile。关键函数/方法:isSourceControlledFileStatus。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/schemas/source-controlled-file.schema.ts -> services/n8n/presentation/n8n-api-types/dto/schemas/source_controlled_file_schema.py

import { z } from 'zod';

const FileTypeSchema = z.enum([
	'credential',
	'workflow',
	'tags',
	'variables',
	'file',
	'folders',
	'project',
]);
export const SOURCE_CONTROL_FILE_TYPE = FileTypeSchema.Values;

const FileStatusSchema = z.enum([
	'new',
	'modified',
	'deleted',
	'created',
	'renamed',
	'conflicted',
	'ignored',
	'staged',
	'unknown',
]);
export const SOURCE_CONTROL_FILE_STATUS = FileStatusSchema.Values;

export type SourceControlledFileStatus = z.infer<typeof FileStatusSchema>;

export function isSourceControlledFileStatus(value: unknown): value is SourceControlledFileStatus {
	return FileStatusSchema.safeParse(value).success;
}

const FileLocationSchema = z.enum(['local', 'remote']);
export const SOURCE_CONTROL_FILE_LOCATION = FileLocationSchema.Values;

const ResourceOwnerSchema = z.object({
	type: z.enum(['personal', 'team']),
	projectId: z.string(),
	projectName: z.string(),
});

export const SourceControlledFileSchema = z.object({
	file: z.string(),
	id: z.string(),
	name: z.string(),
	type: FileTypeSchema,
	status: FileStatusSchema,
	location: FileLocationSchema,
	conflict: z.boolean(),
	updatedAt: z.string(),
	pushed: z.boolean().optional(),
	owner: ResourceOwnerSchema.optional(), // Resource owner can be a personal email or team information
});

export type SourceControlledFile = z.infer<typeof SourceControlledFileSchema>;
