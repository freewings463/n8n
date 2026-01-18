"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/dynamic-node-parameters/base-dynamic-parameters-request.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/dynamic-node-parameters 的模块。导入/依赖:外部:zod、zod-class；内部:n8n-workflow；本地:../schemas/node-version.schema。导出:BaseDynamicParametersRequestDto。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/dynamic-node-parameters/base-dynamic-parameters-request.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/dynamic-node-parameters/base_dynamic_parameters_request_dto.py

import type { INodeCredentials, INodeParameters, INodeTypeNameVersion } from 'n8n-workflow';
import { z } from 'zod';
import { Z } from 'zod-class';

import { nodeVersionSchema } from '../../schemas/node-version.schema';

export class BaseDynamicParametersRequestDto extends Z.class({
	path: z.string(),
	nodeTypeAndVersion: z.object({
		name: z.string(),
		version: nodeVersionSchema,
	}) satisfies z.ZodType<INodeTypeNameVersion>,
	currentNodeParameters: z.record(z.string(), z.any()) satisfies z.ZodType<INodeParameters>,
	methodName: z.string().optional(),
	credentials: z.record(z.string(), z.any()).optional() satisfies z.ZodType<
		INodeCredentials | undefined
	>,
	projectId: z.string().optional(),
}) {}
