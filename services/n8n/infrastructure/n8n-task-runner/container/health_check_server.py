"""
MIGRATION-META:
  source_path: packages/@n8n/task-runner/src/health-check-server.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/task-runner/src 的模块。导入/依赖:外部:无；内部:@n8n/errors；本地:无。导出:HealthCheckServer。关键函数/方法:start、stop、portInUseErrorHandler、reject、resolve。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/task-runner/src/health-check-server.ts -> services/n8n/infrastructure/n8n-task-runner/container/health_check_server.py

import { ApplicationError } from '@n8n/errors';
import { createServer } from 'node:http';

export class HealthCheckServer {
	private server = createServer((_, res) => {
		res.writeHead(200);
		res.end('OK');
	});

	async start(host: string, port: number) {
		return await new Promise<void>((resolve, reject) => {
			const portInUseErrorHandler = (error: NodeJS.ErrnoException) => {
				if (error.code === 'EADDRINUSE') {
					reject(new ApplicationError(`Port ${port} is already in use`));
				} else {
					reject(error);
				}
			};

			this.server.on('error', portInUseErrorHandler);

			this.server.listen(port, host, () => {
				this.server.removeListener('error', portInUseErrorHandler);
				console.log(`Health check server listening on ${host}, port ${port}`);
				resolve();
			});
		});
	}

	async stop() {
		return await new Promise<void>((resolve, reject) => {
			this.server.close((error) => {
				if (error) reject(error);
				else resolve();
			});
		});
	}
}
