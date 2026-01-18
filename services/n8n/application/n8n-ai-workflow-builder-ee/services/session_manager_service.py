"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/session-manager.service.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src 的工作流服务。导入/依赖:外部:@langchain/core/runnables、@langchain/langgraph；内部:@n8n/backend-common、@n8n/di、n8n-workflow、@/tools/builder-tools、@/types/sessions、@/utils/stream-processor；本地:无。导出:SessionManagerService。关键函数/方法:generateThreadId、getCheckpointer、getSessions、getBuilderToolsForDisplay、truncateMessagesAfter。用于封装工作流业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/session-manager.service.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/session_manager_service.py

import { RunnableConfig } from '@langchain/core/runnables';
import { type Checkpoint, MemorySaver } from '@langchain/langgraph';
import { Logger } from '@n8n/backend-common';
import { Service } from '@n8n/di';
import type { INodeTypeDescription } from 'n8n-workflow';

import { getBuilderToolsForDisplay } from '@/tools/builder-tools';
import { isLangchainMessagesArray, LangchainMessage, Session } from '@/types/sessions';
import { formatMessages } from '@/utils/stream-processor';

@Service()
export class SessionManagerService {
	private checkpointer: MemorySaver;

	constructor(
		private readonly parsedNodeTypes: INodeTypeDescription[],
		private readonly logger?: Logger,
	) {
		this.checkpointer = new MemorySaver();
	}

	/**
	 * Generate a thread ID for a given workflow and user
	 */
	static generateThreadId(workflowId?: string, userId?: string): string {
		return workflowId
			? `workflow-${workflowId}-user-${userId ?? new Date().getTime()}`
			: crypto.randomUUID();
	}

	/**
	 * Get the checkpointer instance
	 */
	getCheckpointer(): MemorySaver {
		return this.checkpointer;
	}

	/**
	 * Get sessions for a given workflow and user
	 */
	async getSessions(
		workflowId: string | undefined,
		userId: string | undefined,
	): Promise<{ sessions: Session[] }> {
		// For now, we'll return the current session if we have a workflowId
		// MemorySaver doesn't expose a way to list all threads, so we'll need to
		// track this differently if we want to list all sessions
		const sessions: Session[] = [];

		if (workflowId) {
			const threadId = SessionManagerService.generateThreadId(workflowId, userId);
			const threadConfig: RunnableConfig = {
				configurable: {
					thread_id: threadId,
				},
			};

			try {
				// Try to get the checkpoint for this thread
				const checkpoint = await this.checkpointer.getTuple(threadConfig);

				if (checkpoint?.checkpoint) {
					const rawMessages = checkpoint.checkpoint.channel_values?.messages;
					const messages: LangchainMessage[] = isLangchainMessagesArray(rawMessages)
						? rawMessages
						: [];

					const formattedMessages = formatMessages(
						messages,
						getBuilderToolsForDisplay({
							nodeTypes: this.parsedNodeTypes,
						}),
					);

					sessions.push({
						sessionId: threadId,
						messages: formattedMessages,
						lastUpdated: checkpoint.checkpoint.ts,
					});
				}
			} catch (error) {
				// Thread doesn't exist yet
				this.logger?.debug('No session found for workflow:', { workflowId, error });
			}
		}

		return { sessions };
	}

	/**
	 * Truncate all messages including and after the message with the specified messageId in metadata.
	 * Used when restoring to a previous version.
	 *
	 * @param workflowId - The workflow ID
	 * @param userId - The user ID
	 * @param messageId - The messageId to find in HumanMessage's additional_kwargs. Messages from this
	 *                    point onward (including the message with this messageId) will be removed.
	 * @returns True if truncation was successful, false if thread or message not found
	 */
	async truncateMessagesAfter(
		workflowId: string,
		userId: string | undefined,
		messageId: string,
	): Promise<boolean> {
		const threadId = SessionManagerService.generateThreadId(workflowId, userId);
		const threadConfig: RunnableConfig = {
			configurable: {
				thread_id: threadId,
			},
		};

		try {
			const checkpointTuple = await this.checkpointer.getTuple(threadConfig);

			if (!checkpointTuple?.checkpoint) {
				this.logger?.debug('No checkpoint found for truncation', { threadId, messageId });
				return false;
			}

			const rawMessages = checkpointTuple.checkpoint.channel_values?.messages;
			if (!isLangchainMessagesArray(rawMessages)) {
				this.logger?.debug('No valid messages found for truncation', { threadId, messageId });
				return false;
			}

			// Find the index of the message with the target messageId in additional_kwargs
			const msgIndex = rawMessages.findIndex(
				(msg) => msg.additional_kwargs?.messageId === messageId,
			);

			if (msgIndex === -1) {
				this.logger?.debug('Message with messageId not found', { threadId, messageId });
				return false;
			}

			// Keep messages before the target message (excluding the target message)
			const truncatedMessages = rawMessages.slice(0, msgIndex);

			// Create updated checkpoint with truncated messages
			const updatedCheckpoint: Checkpoint = {
				...checkpointTuple.checkpoint,
				channel_values: {
					...checkpointTuple.checkpoint.channel_values,
					messages: truncatedMessages,
				},
			};

			// Put the updated checkpoint back with metadata indicating this is an update
			const metadata = checkpointTuple.metadata ?? {
				source: 'update' as const,
				step: -1,
				parents: {},
			};

			await this.checkpointer.put(threadConfig, updatedCheckpoint, metadata);

			this.logger?.debug('Messages truncated successfully', {
				threadId,
				messageId,
				originalCount: rawMessages.length,
				newCount: truncatedMessages.length,
			});

			return true;
		} catch (error) {
			this.logger?.error('Failed to truncate messages', { threadId, messageId, error });
			return false;
		}
	}
}
