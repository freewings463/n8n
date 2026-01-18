"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ReActAgent/prompt.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:PREFIX、SUFFIX_CHAT、SUFFIX、HUMAN_MESSAGE_TEMPLATE。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ReActAgent/prompt.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/agents/ReActAgent/prompt.py

export const PREFIX =
	'Answer the following questions as best you can. You have access to the following tools:';

export const SUFFIX_CHAT =
	'Begin! Reminder to always use the exact characters `Final Answer` when responding.';

export const SUFFIX = `Begin!

	Question: {input}
	Thought:{agent_scratchpad}`;

export const HUMAN_MESSAGE_TEMPLATE = '{input}\n\n{agent_scratchpad}';
