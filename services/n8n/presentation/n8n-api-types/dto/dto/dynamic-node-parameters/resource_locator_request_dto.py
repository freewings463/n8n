"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/dynamic-node-parameters/resource-locator-request.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/dynamic-node-parameters 的模块。导入/依赖:外部:zod；内部:无；本地:./base-dynamic-parameters-request.dto。导出:ResourceLocatorRequestDto。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/dynamic-node-parameters/resource-locator-request.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/dynamic-node-parameters/resource_locator_request_dto.py

import { z } from 'zod';

import { BaseDynamicParametersRequestDto } from './base-dynamic-parameters-request.dto';

export class ResourceLocatorRequestDto extends BaseDynamicParametersRequestDto.extend({
	methodName: z.string(),
	filter: z.string().optional(),
	paginationToken: z.string().optional(),
}) {}
