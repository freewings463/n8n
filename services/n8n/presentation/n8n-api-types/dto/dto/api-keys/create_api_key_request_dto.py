"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/api-keys/create-api-key-request.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/api-keys 的模块。导入/依赖:外部:zod；内部:无；本地:./update-api-key-request.dto。导出:CreateApiKeyRequestDto。关键函数/方法:isTimeNullOrInFuture。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/api-keys/create-api-key-request.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/api-keys/create_api_key_request_dto.py

import { z } from 'zod';

import { UpdateApiKeyRequestDto } from './update-api-key-request.dto';

const isTimeNullOrInFuture = (value: number | null) => {
	if (!value) return true;
	return value > Date.now() / 1000;
};

export class CreateApiKeyRequestDto extends UpdateApiKeyRequestDto.extend({
	expiresAt: z
		.number()
		.nullable()
		.refine(isTimeNullOrInFuture, { message: 'Expiration date must be in the future or null' }),
}) {}
