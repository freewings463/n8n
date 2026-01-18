"""
MIGRATION-META:
  source_path: packages/cli/src/modules/chat-hub/dto/chat-models-request.dto.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/chat-hub/dto 的模块。导入/依赖:外部:zod-class；内部:@n8n/api-types；本地:无。导出:ChatModelsRequestDto。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/chat-hub/dto/chat-models-request.dto.ts -> services/n8n/application/cli/services/modules/chat-hub/dto/chat_models_request_dto.py

import { chatModelsRequestSchema } from '@n8n/api-types';
import { Z } from 'zod-class';

export class ChatModelsRequestDto extends Z.class(chatModelsRequestSchema.shape) {}
