"""
MIGRATION-META:
  source_path: packages/@n8n/imap/src/helpers/get-message.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/imap/src/helpers 的模块。导入/依赖:外部:无；内部:无；本地:../types。导出:无。关键函数/方法:getMessage、messageOnBody、streamOnData、messageOnAttributes、messageOnEnd、resolve。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/imap/src/helpers/get-message.ts -> services/n8n/tests/n8n-imap/unit/helpers/get_message.py

import {
	parseHeader,
	type ImapMessage,
	type ImapMessageBodyInfo,
	type ImapMessageAttributes,
} from 'imap';

import type { Message, MessageBodyPart } from '../types';

/**
 * Given an 'ImapMessage' from the node-imap library, retrieves the `Message`
 */
export async function getMessage(
	/** an ImapMessage from the node-imap library */
	message: ImapMessage,
): Promise<Message> {
	return await new Promise((resolve) => {
		let attributes: ImapMessageAttributes;
		const parts: MessageBodyPart[] = [];

		const messageOnBody = (stream: NodeJS.ReadableStream, info: ImapMessageBodyInfo) => {
			let body: string = '';

			const streamOnData = (chunk: Buffer) => {
				body += chunk.toString('utf8');
			};

			stream.on('data', streamOnData);
			stream.once('end', () => {
				stream.removeListener('data', streamOnData);

				parts.push({
					which: info.which,
					size: info.size,
					body: /^HEADER/g.test(info.which) ? parseHeader(body) : body,
				});
			});
		};

		const messageOnAttributes = (attrs: ImapMessageAttributes) => {
			attributes = attrs;
		};

		const messageOnEnd = () => {
			message.removeListener('body', messageOnBody);
			message.removeListener('attributes', messageOnAttributes);
			resolve({ attributes, parts });
		};

		message.on('body', messageOnBody);
		message.once('attributes', messageOnAttributes);
		message.once('end', messageOnEnd);
	});
}
