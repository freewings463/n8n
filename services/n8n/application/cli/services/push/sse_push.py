"""
MIGRATION-META:
  source_path: packages/cli/src/push/sse.push.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/push 的模块。导入/依赖:外部:无；内部:@n8n/db、@n8n/di；本地:./abstract.push、./types。导出:SSEPush。关键函数/方法:add、removeClient、close、sendToOneConnection、ping。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/push/sse.push.ts -> services/n8n/application/cli/services/push/sse_push.py

import type { User } from '@n8n/db';
import { Service } from '@n8n/di';

import { AbstractPush } from './abstract.push';
import type { PushRequest, PushResponse } from './types';

type Connection = { req: PushRequest; res: PushResponse };

@Service()
export class SSEPush extends AbstractPush<Connection> {
	add(pushRef: string, userId: User['id'], connection: Connection) {
		const { req, res } = connection;

		// Initialize the connection
		req.socket.setTimeout(0);
		req.socket.setNoDelay(true);
		req.socket.setKeepAlive(true);
		res.setHeader('Content-Type', 'text/event-stream; charset=UTF-8');
		res.setHeader('Cache-Control', 'no-cache');
		res.setHeader('Connection', 'keep-alive');
		res.writeHead(200);
		res.write(':ok\n\n');
		res.flush();

		super.add(pushRef, userId, connection);

		// When the client disconnects, remove the client
		const removeClient = () => this.remove(pushRef);
		req.once('end', removeClient);
		req.once('close', removeClient);
		res.once('finish', removeClient);
	}

	protected close({ res }: Connection) {
		res.end();
	}

	protected sendToOneConnection(connection: Connection, data: string) {
		const { res } = connection;
		res.write('data: ' + data + '\n\n');
		res.flush();
	}

	protected ping({ res }: Connection) {
		res.write(':ping\n\n');
		res.flush();
	}
}
