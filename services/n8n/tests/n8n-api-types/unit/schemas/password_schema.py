"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/schemas/password.schema.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/api-types/src/schemas 的模块。导入/依赖:外部:zod；内部:无；本地:无。导出:passwordSchema。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/schemas/password.schema.ts -> services/n8n/tests/n8n-api-types/unit/schemas/password_schema.py

import { z } from 'zod';

// TODO: Delete these from `cli` after all password-validation code starts using this schema
const minLength = 8;
const maxLength = 64;

export const passwordSchema = z
	.string()
	.min(minLength, `Password must be ${minLength} to ${maxLength} characters long.`)
	.max(maxLength, `Password must be ${minLength} to ${maxLength} characters long.`)
	.refine((password) => /\d/.test(password), {
		message: 'Password must contain at least 1 number.',
	})
	.refine((password) => /[A-Z]/.test(password), {
		message: 'Password must contain at least 1 uppercase letter.',
	});
