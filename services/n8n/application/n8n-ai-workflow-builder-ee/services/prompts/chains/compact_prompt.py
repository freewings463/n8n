"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/compact.prompt.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/prompts/chains 的工作流模块。导入/依赖:外部:@langchain/core/prompts；内部:无；本地:无。导出:compactPromptTemplate。关键函数/方法:无。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/prompts/chains/compact.prompt.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/prompts/chains/compact_prompt.py

import { PromptTemplate } from '@langchain/core/prompts';

/** Template for summarizing multi-turn conversations into a structured format */
export const compactPromptTemplate = PromptTemplate.fromTemplate(
	`Please summarize the following conversation between a user and an AI assistant building an n8n workflow:

<previous_summary>
{previousSummary}
</previous_summary>

<conversation>
{conversationText}
</conversation>

Provide a structured summary that captures the key points, decisions made, current state of the workflow, and suggested next steps.`,
);
