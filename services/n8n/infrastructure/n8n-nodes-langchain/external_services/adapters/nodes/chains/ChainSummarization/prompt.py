"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/chains/ChainSummarization/prompt.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/chains/ChainSummarization 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:REFINE_PROMPT_TEMPLATE、DEFAULT_PROMPT_TEMPLATE。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/chains/ChainSummarization/prompt.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/chains/ChainSummarization/prompt.py

export const REFINE_PROMPT_TEMPLATE = `Your job is to produce a final summary
We have provided an existing summary up to a certain point: "{existing_answer}"
We have the opportunity to refine the existing summary
(only if needed) with some more context below.
------------
"{text}"
------------

Given the new context, refine the original summary
If the context isn't useful, return the original summary.

REFINED SUMMARY:`;

export const DEFAULT_PROMPT_TEMPLATE = `Write a concise summary of the following:


"{text}"


CONCISE SUMMARY:`;
