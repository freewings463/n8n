"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/output_parser/OutputParserAutofixing/prompt.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/output_parser/OutputParserAutofixing 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:NAIVE_FIX_PROMPT。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/output_parser/OutputParserAutofixing/prompt.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/output_parser/OutputParserAutofixing/prompt.py

export const NAIVE_FIX_PROMPT = `Instructions:
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
