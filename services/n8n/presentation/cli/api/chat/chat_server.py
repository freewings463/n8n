"""
MIGRATION-META:
  source_path: packages/cli/src/chat/chat-server.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/chat 的模块。导入/依赖:外部:express、ws；内部:@n8n/di、@n8n/decorators；本地:./chat-service、./chat-service.types。导出:ChatServer。关键函数/方法:setup、attachToApp、shutdown。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected Express Request/Response adapter/helper
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/chat/chat-server.ts -> services/n8n/presentation/cli/api/chat/chat_server.py

import { Service } from '@n8n/di';
import { OnShutdown } from '@n8n/decorators';
import type { Application } from 'express';
import type { Server as HttpServer } from 'http';
import { ServerResponse } from 'http';
import { parse as parseUrl } from 'url';
import type { WebSocket } from 'ws';
import { Server as WebSocketServer } from 'ws';

import { ChatService } from './chat-service';
import type { ChatRequest } from './chat-service.types';

interface ExpressApplication extends Application {
	handle: (req: any, res: any) => void;
}

@Service()
export class ChatServer {
	private readonly wsServer = new WebSocketServer({ noServer: true });

	constructor(private readonly chatService: ChatService) {}

	setup(server: HttpServer, app: Application) {
		server.on('upgrade', (req: ChatRequest, socket, head) => {
			const parsedUrl = parseUrl(req.url ?? '');

			if (parsedUrl.pathname?.startsWith('/chat')) {
				this.wsServer.handleUpgrade(req, socket, head, (ws) => {
					this.attachToApp(req, ws, app as ExpressApplication);
				});
			}
		});

		app.use('/chat', async (req: ChatRequest) => {
			await this.chatService.startSession(req);
		});
	}

	private attachToApp(req: ChatRequest, ws: WebSocket, app: ExpressApplication) {
		req.ws = ws;
		const res = new ServerResponse(req);
		res.writeHead = (statusCode) => {
			if (statusCode > 200) ws.close();
			return res;
		};

		app.handle(req, res);
	}

	@OnShutdown()
	shutdown() {
		this.wsServer.close();
	}
}
