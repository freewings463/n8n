"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/chains/conversation-compact.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/chains 的工作流模块。导入/依赖:外部:@langchain/core/…/chat_models、@langchain/core/messages、zod；内部:@/prompts/…/compact.prompt；本地:无。导出:无。关键函数/方法:conversationCompactChain。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/chains/conversation-compact.ts -> services/n8n/tests/n8n-ai-workflow-builder-ee/unit/chains/conversation_compact.py

import type { BaseChatModel } from '@langchain/core/language_models/chat_models';
import type { BaseMessage } from '@langchain/core/messages';
import { AIMessage, HumanMessage } from '@langchain/core/messages';
import z from 'zod';

import { compactPromptTemplate } from '@/prompts/chains/compact.prompt';

export async function conversationCompactChain(
	llm: BaseChatModel,
	messages: BaseMessage[],
	previousSummary: string = '',
) {
	// Use structured output for consistent summary format
	const CompactedSession = z.object({
		summary: z.string().describe('A concise summary of the conversation so far'),
		key_decisions: z.array(z.string()).describe('List of key decisions and actions taken'),
		current_state: z.string().describe('Description of the current workflow state'),
		next_steps: z.string().describe('Suggested next steps based on the conversation'),
	});

	const modelWithStructure = llm.withStructuredOutput(CompactedSession);

	// Format messages for summarization
	const conversationText = messages
		.map((msg) => {
			if (msg instanceof HumanMessage) {
				// eslint-disable-next-line @typescript-eslint/no-base-to-string, @typescript-eslint/restrict-template-expressions
				return `User: ${msg.content}`;
			} else if (msg instanceof AIMessage) {
				if (typeof msg.content === 'string') {
					return `Assistant: ${msg.content}`;
				} else {
					return 'Assistant: Used tools';
				}
			}

			return '';
		})
		.filter(Boolean)
		.join('\n');

	const compactPrompt = await compactPromptTemplate.invoke({
		previousSummary,
		conversationText,
	});

	const structuredOutput = await modelWithStructure.invoke(compactPrompt);

	const formattedSummary = `## Previous Conversation Summary

**Summary:** ${structuredOutput.summary}

**Key Decisions:**
${(structuredOutput.key_decisions as string[]).map((d: string) => `- ${d}`).join('\n')}

**Current State:** ${structuredOutput.current_state}

**Next Steps:** ${structuredOutput.next_steps}`;

	return {
		success: true,
		summary: structuredOutput,
		summaryPlain: formattedSummary,
	};
}
