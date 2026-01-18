"""
MIGRATION-META:
  source_path: packages/cli/src/collaboration/collaboration.message.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/collaboration 的模块。导入/依赖:外部:zod；内部:无；本地:无。导出:CollaborationMessage、workflowOpenedMessageSchema、workflowClosedMessageSchema、writeAccessRequestedMessageSchema、writeAccessReleaseRequestedMessageSchema、writeAccessHeartbeatMessageSchema、workflowMessageSchema、WorkflowOpenedMessage 等6项。关键函数/方法:parseWorkflowMessage。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Collaboration message contracts -> presentation/dto/collaboration
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/collaboration/collaboration.message.ts -> services/n8n/presentation/cli/dto/collaboration/collaboration_message.py

import { z } from 'zod';

export type CollaborationMessage =
	| WorkflowOpenedMessage
	| WorkflowClosedMessage
	| WriteAccessRequestedMessage
	| WriteAccessReleaseRequestedMessage
	| WriteAccessHeartbeatMessage;

export const workflowOpenedMessageSchema = z
	.object({
		type: z.literal('workflowOpened'),
		workflowId: z.string().min(1),
	})
	.strict();

export const workflowClosedMessageSchema = z
	.object({
		type: z.literal('workflowClosed'),
		workflowId: z.string().min(1),
	})
	.strict();

export const writeAccessRequestedMessageSchema = z
	.object({
		type: z.literal('writeAccessRequested'),
		workflowId: z.string().min(1),
	})
	.strict();

export const writeAccessReleaseRequestedMessageSchema = z
	.object({
		type: z.literal('writeAccessReleaseRequested'),
		workflowId: z.string().min(1),
	})
	.strict();

export const writeAccessHeartbeatMessageSchema = z
	.object({
		type: z.literal('writeAccessHeartbeat'),
		workflowId: z.string().min(1),
	})
	.strict();

export const workflowMessageSchema = z.discriminatedUnion('type', [
	workflowOpenedMessageSchema,
	workflowClosedMessageSchema,
	writeAccessRequestedMessageSchema,
	writeAccessReleaseRequestedMessageSchema,
	writeAccessHeartbeatMessageSchema,
]);

export type WorkflowOpenedMessage = z.infer<typeof workflowOpenedMessageSchema>;

export type WorkflowClosedMessage = z.infer<typeof workflowClosedMessageSchema>;

export type WriteAccessRequestedMessage = z.infer<typeof writeAccessRequestedMessageSchema>;

export type WriteAccessReleaseRequestedMessage = z.infer<
	typeof writeAccessReleaseRequestedMessageSchema
>;

export type WriteAccessHeartbeatMessage = z.infer<typeof writeAccessHeartbeatMessageSchema>;

export type WorkflowMessage = z.infer<typeof workflowMessageSchema>;

/**
 * Parses the given message and ensure it's of type WorkflowMessage
 */
export const parseWorkflowMessage = async (msg: unknown) => {
	return await workflowMessageSchema.parseAsync(msg);
};
