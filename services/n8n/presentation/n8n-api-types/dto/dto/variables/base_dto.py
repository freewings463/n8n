"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/variables/base.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/variables 的模块。导入/依赖:外部:zod、zod-class；内部:无；本地:无。导出:KEY_NAME_REGEX、KEY_MAX_LENGTH、VALUE_MAX_LENGTH、TYPE_ENUM、TYPE_DEFAULT、variableKeySchema、variableValueSchema、variableTypeSchema 等1项。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/variables/base.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/variables/base_dto.py

import { z } from 'zod';
import { Z } from 'zod-class';

export const KEY_NAME_REGEX = /^[A-Za-z0-9_]+$/;
export const KEY_MAX_LENGTH = 50;
export const VALUE_MAX_LENGTH = 1000;
export const TYPE_ENUM = ['string'] as const;
export const TYPE_DEFAULT: (typeof TYPE_ENUM)[number] = 'string';

export const variableKeySchema = z
	.string()
	.min(1, 'key must be at least 1 character long')
	.max(KEY_MAX_LENGTH, 'key cannot be longer than 50 characters')
	.regex(KEY_NAME_REGEX, 'key can only contain characters A-Za-z0-9_');

export const variableValueSchema = z
	.string()
	.max(VALUE_MAX_LENGTH, `value cannot be longer than ${VALUE_MAX_LENGTH} characters`);

export const variableTypeSchema = z.enum(TYPE_ENUM).default(TYPE_DEFAULT);

export class BaseVariableRequestDto extends Z.class({
	key: variableKeySchema,
	type: variableTypeSchema,
	value: variableValueSchema,
}) {}
