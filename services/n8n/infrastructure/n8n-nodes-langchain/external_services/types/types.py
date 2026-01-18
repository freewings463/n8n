"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/types/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/types 的类型。导入/依赖:外部:zod；内部:无；本地:无。导出:OpenAICompatibleCredential、ZodObjectAny。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/types/types.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/types/types.py

import type { z } from 'zod';

export type OpenAICompatibleCredential = { apiKey: string; url: string };

export type ZodObjectAny = z.ZodObject<any, any, any, any>;
