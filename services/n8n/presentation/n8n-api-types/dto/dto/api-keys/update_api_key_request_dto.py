"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/api-keys/update-api-key-request.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/api-keys 的模块。导入/依赖:外部:xss、zod、zod-class；内部:无；本地:../schemas/scopes.schema。导出:UpdateApiKeyRequestDto。关键函数/方法:xssCheck、xss。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/api-keys/update-api-key-request.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/api-keys/update_api_key_request_dto.py

import xss from 'xss';
import { z } from 'zod';
import { Z } from 'zod-class';

import { scopesSchema } from '../../schemas/scopes.schema';

const xssCheck = (value: string) =>
	value ===
	xss(value, {
		whiteList: {},
	});

export class UpdateApiKeyRequestDto extends Z.class({
	label: z.string().max(50).min(1).refine(xssCheck),
	scopes: scopesSchema,
}) {}
