"""
MIGRATION-META:
  source_path: packages/@n8n/imap/src/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/imap/src 的类型。导入/依赖:外部:imap；内部:无；本地:无。导出:ImapSimpleOptions、MessagePart、MessageBodyPart、Message、SearchCriteria。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/imap treated as external service client library
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/imap/src/types.ts -> services/n8n/infrastructure/n8n-imap/external_services/clients/types.py

import type { Config, ImapMessageBodyInfo, ImapMessageAttributes } from 'imap';

export interface ImapSimpleOptions {
	/** Options to pass to node-imap constructor. */
	imap: Config;

	/** Server event emitted when new mail arrives in the currently open mailbox. */
	onMail?: ((numNewMail: number) => void) | undefined;

	/** Server event emitted when a message was expunged externally. seqNo is the sequence number (instead of the unique UID) of the message that was expunged. If you are caching sequence numbers, all sequence numbers higher than this value MUST be decremented by 1 in order to stay synchronized with the server and to keep correct continuity. */
	onExpunge?: ((seqNo: number) => void) | undefined;

	/** Server event emitted when message metadata (e.g. flags) changes externally. */
	onUpdate?:
		| ((seqNo: number, info: { num: number | undefined; text: unknown }) => void)
		| undefined;
}

export interface MessagePart {
	partID: string;
	encoding: 'BASE64' | 'QUOTED-PRINTABLE' | '7BIT' | '8BIT' | 'BINARY' | 'UUENCODE';
	type: 'TEXT';
	subtype: string;
	params?: {
		charset?: string;
	};
	disposition?: {
		type: string;
	};
}

export interface MessageBodyPart extends ImapMessageBodyInfo {
	/** string type where which=='TEXT', complex Object where which=='HEADER' */
	body: string | object;
}

export interface Message {
	attributes: ImapMessageAttributes;
	parts: MessageBodyPart[];
	seqNo?: number;
}

export type SearchCriteria = string | [string, string];
