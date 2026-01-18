"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Gmail/v2/utils/draft.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Gmail 的工具。导入/依赖:外部:@utils/sendAndWait/interfaces；内部:n8n-workflow；本地:../../GenericFunctions。导出:无。关键函数/方法:setEmailReplyHeaders、setThreadHeaders、addThreadHeadersToEmail。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Gmail/v2/utils/draft.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Gmail/v2/utils/draft.py

import type { IExecuteFunctions } from 'n8n-workflow';

import type { IEmail } from '@utils/sendAndWait/interfaces';

import { googleApiRequest } from '../../GenericFunctions';

function setEmailReplyHeaders(email: IEmail, messageId: string | undefined): void {
	if (messageId) {
		email.inReplyTo = messageId;
		email.references = messageId;
	}
}

function setThreadHeaders(
	email: IEmail,
	thread: { messages: Array<{ payload: { headers: Array<{ name: string; value: string }> } }> },
): void {
	if (thread?.messages) {
		const lastMessage = thread.messages.length - 1;
		const messageId = thread.messages[lastMessage].payload.headers.find(
			(header: { name: string; value: string }) =>
				header.name.toLowerCase().includes('message') && header.name.toLowerCase().includes('id'),
		)?.value;

		setEmailReplyHeaders(email, messageId);
	}
}

/**
 * Adds inReplyTo and reference headers to the email if threadId is provided.
 */
export async function addThreadHeadersToEmail(
	this: IExecuteFunctions,
	email: IEmail,
	threadId: string,
): Promise<void> {
	const thread = await googleApiRequest.call(
		this,
		'GET',
		`/gmail/v1/users/me/threads/${threadId}`,
		{},
		{ format: 'metadata', metadataHeaders: ['Message-ID'] },
	);

	setThreadHeaders(email, thread);
}
