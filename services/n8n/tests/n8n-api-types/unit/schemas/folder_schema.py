"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/schemas/folder.schema.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/api-types/src/schemas 的模块。导入/依赖:外部:zod；内部:无；本地:无。导出:folderNameSchema、folderIdSchema。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/schemas/folder.schema.ts -> services/n8n/tests/n8n-api-types/unit/schemas/folder_schema.py

import { z } from 'zod';

const illegalCharacterRegex = /[[\]^\\/:*?"<>|]/;
const dotsOnlyRegex = /^\.+$/;
const FOLDER_NAME_MAX_LENGTH = 128;

export const folderNameSchema = z
	.string()
	.trim()
	.superRefine((name, ctx) => {
		if (name === '') {
			ctx.addIssue({
				code: z.ZodIssueCode.custom,
				message: 'Folder name cannot be empty',
			});
			return;
		}

		if (illegalCharacterRegex.test(name)) {
			ctx.addIssue({
				code: z.ZodIssueCode.custom,
				message: 'Folder name contains invalid characters',
			});
			return;
		}

		if (dotsOnlyRegex.test(name)) {
			ctx.addIssue({
				code: z.ZodIssueCode.custom,
				message: 'Folder name cannot consist of dots only',
			});
			return;
		}

		if (name.startsWith('.')) {
			ctx.addIssue({
				code: z.ZodIssueCode.custom,
				message: 'Folder name cannot start with a dot',
			});
		}
	})
	.pipe(
		z.string().max(FOLDER_NAME_MAX_LENGTH, {
			message: `Folder name cannot be longer than ${FOLDER_NAME_MAX_LENGTH} characters`,
		}),
	);
export const folderIdSchema = z.string().max(36);
