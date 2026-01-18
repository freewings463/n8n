"""
MIGRATION-META:
  source_path: packages/@n8n/api-types/src/dto/ai/ai-ask-request.dto.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/api-types/src/dto/ai 的模块。导入/依赖:外部:zod、zod-class；内部:@n8n_io/ai-assistant-sdk；本地:无。导出:AiAskRequestDto。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/api-types treated as presentation DTO contracts
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/api-types/src/dto/ai/ai-ask-request.dto.ts -> services/n8n/presentation/n8n-api-types/dto/dto/ai/ai_ask_request_dto.py

import type { AiAssistantSDK, SchemaType } from '@n8n_io/ai-assistant-sdk';
import { z } from 'zod';
import { Z } from 'zod-class';

// Note: This is copied from the sdk, since this type is not exported
type Schema = {
	type: SchemaType;
	key?: string;
	value: string | Schema[];
	path: string;
};

// Create a lazy validator to handle the recursive type
const schemaValidator: z.ZodType<Schema> = z.lazy(() =>
	z.object({
		type: z.enum([
			'string',
			'number',
			'boolean',
			'bigint',
			'symbol',
			'array',
			'object',
			'function',
			'null',
			'undefined',
		]),
		key: z.string().optional(),
		value: z.union([z.string(), z.lazy(() => schemaValidator.array())]),
		path: z.string(),
	}),
);

export class AiAskRequestDto
	extends Z.class({
		question: z.string(),
		context: z.object({
			schema: z.array(
				z.object({
					nodeName: z.string(),
					schema: schemaValidator,
				}),
			),
			inputSchema: z.object({
				nodeName: z.string(),
				schema: schemaValidator,
			}),
			pushRef: z.string(),
			ndvPushRef: z.string(),
		}),
		forNode: z.string(),
	})
	implements AiAssistantSDK.AskAiRequestPayload {}
