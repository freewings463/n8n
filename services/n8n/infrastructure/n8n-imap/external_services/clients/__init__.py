"""
MIGRATION-META:
  source_path: packages/@n8n/imap/src/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/imap/src 的入口。导入/依赖:外部:imap；内部:无；本地:./errors、./imap-simple、./types。再导出:./imap-simple、./errors。导出:getParts。关键函数/方法:connect、cleanUp、imapOnReady、resolve、imapOnError、reject、imapOnEnd、imapOnClose、getParts。用于汇总导出并完成该模块模块初始化、注册或装配。注释目标:eslint-disable @typescript-eslint/no-unsafe-member-access。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/imap treated as external service client library
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/imap/src/index.ts -> services/n8n/infrastructure/n8n-imap/external_services/clients/__init__.py

/* eslint-disable @typescript-eslint/no-unsafe-member-access */

import Imap from 'imap';

import { ConnectionClosedError, ConnectionEndedError, ConnectionTimeoutError } from './errors';
import { ImapSimple } from './imap-simple';
import type { ImapSimpleOptions, MessagePart } from './types';

/**
 * Connect to an Imap server, returning an ImapSimple instance, which is a wrapper over node-imap to simplify it's api for common use cases.
 */
export async function connect(options: ImapSimpleOptions): Promise<ImapSimple> {
	const authTimeout = options.imap.authTimeout ?? 2000;
	options.imap.authTimeout = authTimeout;

	const imap = new Imap(options.imap);

	return await new Promise<ImapSimple>((resolve, reject) => {
		const cleanUp = () => {
			imap.removeListener('ready', imapOnReady);
			imap.removeListener('error', imapOnError);
			imap.removeListener('close', imapOnClose);
			imap.removeListener('end', imapOnEnd);
		};

		const imapOnReady = () => {
			cleanUp();
			resolve(new ImapSimple(imap));
		};

		const imapOnError = (e: Error & { source?: string }) => {
			if (e.source === 'timeout-auth') {
				e = new ConnectionTimeoutError(authTimeout);
			}

			cleanUp();
			reject(e);
		};

		const imapOnEnd = () => {
			cleanUp();
			reject(new ConnectionEndedError());
		};

		const imapOnClose = () => {
			cleanUp();
			reject(new ConnectionClosedError());
		};

		imap.once('ready', imapOnReady);
		imap.once('error', imapOnError);
		imap.once('close', imapOnClose);
		imap.once('end', imapOnEnd);

		if (options.onMail) {
			imap.on('mail', options.onMail);
		}

		if (options.onExpunge) {
			imap.on('expunge', options.onExpunge);
		}

		if (options.onUpdate) {
			imap.on('update', options.onUpdate);
		}

		imap.connect();
	});
}

/**
 * Given the `message.attributes.struct`, retrieve a flattened array of `parts` objects that describe the structure of
 * the different parts of the message's body. Useful for getting a simple list to iterate for the purposes of,
 * for example, finding all attachments.
 *
 * Code taken from http://stackoverflow.com/questions/25247207/how-to-read-and-save-attachments-using-node-imap
 *
 * @returns {Array} a flattened array of `parts` objects that describe the structure of the different parts of the
 *  message's body
 */
export function getParts(
	/** The `message.attributes.struct` value from the message you wish to retrieve parts for. */
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	struct: any,
	/** The list of parts to push to. */
	parts: MessagePart[] = [],
): MessagePart[] {
	for (let i = 0; i < struct.length; i++) {
		if (Array.isArray(struct[i])) {
			getParts(struct[i], parts);
		} else if (struct[i].partID) {
			parts.push(struct[i] as MessagePart);
		}
	}
	return parts;
}

export * from './imap-simple';
export * from './errors';
export type * from './types';
