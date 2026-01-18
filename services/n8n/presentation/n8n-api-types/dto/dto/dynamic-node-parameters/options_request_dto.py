"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/dynamic-node-parameters/options-request.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/dynamic-node-parameters 的模块。导入/依赖:外部:zod；内部:n8n-workflow；本地:./base-dynamic-parameters-request.dto。导出:OptionsRequestDto。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/dynamic-node-parameters/options-request.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/dynamic-node-parameters/options_request_dto.py

import type { ILoadOptions } from 'n8n-workflow';
import { z } from 'zod';

import { BaseDynamicParametersRequestDto } from './base-dynamic-parameters-request.dto';

export class OptionsRequestDto extends BaseDynamicParametersRequestDto.extend({
	loadOptions: z
		.object({
			routing: z
				.object({
					operations: z.any().optional(),
					output: z.any().optional(),
					request: z.any().optional(),
				})
				.optional(),
		})
		.optional() as z.ZodType<ILoadOptions | undefined>,
}) {}
