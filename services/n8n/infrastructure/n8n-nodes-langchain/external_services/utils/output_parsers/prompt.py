"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/utils/output_parsers/prompt.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/utils/output_parsers 的工具。导入/依赖:外部:@langchain/core/prompts；内部:无；本地:无。导出:NAIVE_FIX_TEMPLATE、NAIVE_FIX_PROMPT。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/utils/output_parsers/prompt.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/utils/output_parsers/prompt.py

import { PromptTemplate } from '@langchain/core/prompts';

export const NAIVE_FIX_TEMPLATE = `Instructions:
--------------
{instructions}
--------------
Completion:
--------------
{completion}
--------------

Above, the Completion did not satisfy the constraints given in the Instructions.
Error:
--------------
{error}
--------------

Please try again. Please only respond with an answer that satisfies the constraints laid out in the Instructions:`;

export const NAIVE_FIX_PROMPT = PromptTemplate.fromTemplate(NAIVE_FIX_TEMPLATE);
