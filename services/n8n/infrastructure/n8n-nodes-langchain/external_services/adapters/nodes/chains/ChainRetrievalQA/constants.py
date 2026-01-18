"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/chains/ChainRetrievalQA/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/chains/ChainRetrievalQA 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:SYSTEM_PROMPT_TEMPLATE、LEGACY_INPUT_TEMPLATE_KEY、INPUT_TEMPLATE_KEY、systemPromptOption。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/chains/ChainRetrievalQA/constants.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/chains/ChainRetrievalQA/constants.py

import type { INodeProperties } from 'n8n-workflow';

export const SYSTEM_PROMPT_TEMPLATE = `You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
----------------
Context: {context}`;

// Due to the refactoring in version 1.5, the variable name {question} needed to be changed to {input} in the prompt template.
export const LEGACY_INPUT_TEMPLATE_KEY = 'question';
export const INPUT_TEMPLATE_KEY = 'input';

export const systemPromptOption: INodeProperties = {
	displayName: 'System Prompt Template',
	name: 'systemPromptTemplate',
	type: 'string',
	default: SYSTEM_PROMPT_TEMPLATE,
	typeOptions: {
		rows: 6,
	},
};
