"""
MIGRATION-META:
  source_path: packages/testing/containers/helpers/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/containers/helpers 的模块。导入/依赖:外部:node:timers/promises、testcontainers；内部:无；本地:无。导出:createElapsedLogger、createSilentLogConsumer。关键函数/方法:createElapsedLogger、elapsed、createSilentLogConsumer、consumer、throwWithLogs、pollContainerHttpEndpoint。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected external HTTP client usage -> infrastructure/external_services/clients
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/containers/helpers/utils.ts -> services/n8n/infrastructure/testing/external_services/clients/containers/helpers/utils.py

import { setTimeout as wait } from 'node:timers/promises';
import type { Readable } from 'stream';
import type { StartedTestContainer } from 'testcontainers';

/**
 * Create a logger that prefixes messages with elapsed time since creation.
 */
export function createElapsedLogger(prefix: string) {
	const startTime = Date.now();

	return (message: string) => {
		const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
		console.log(`[${prefix} +${elapsed}s] ${message}`);
	};
}

/**
 * Create a log consumer that does not log to the console.
 * Logs are collected in memory and can be output on error.
 */
export function createSilentLogConsumer() {
	const logs: string[] = [];

	const consumer = (stream: Readable) => {
		stream.on('data', (chunk: Buffer | string) => {
			logs.push(chunk.toString().trim());
		});
	};

	const throwWithLogs = (error: unknown): never => {
		if (logs.length > 0) {
			console.error('\n--- Container Logs ---');
			console.error(logs.join('\n'));
			console.error('---------------------\n');
		}
		throw error;
	};

	return { consumer, throwWithLogs };
}

/**
 * Polls a container's HTTP endpoint until it returns a 200 status.
 * Logs a warning if the endpoint does not return 200 within the specified timeout.
 *
 * @param container The started container.
 * @param endpoint The HTTP health check endpoint (e.g., '/healthz/readiness').
 * @param timeoutMs Total timeout in milliseconds (default: 60,000ms).
 */
export async function pollContainerHttpEndpoint(
	container: StartedTestContainer,
	endpoint: string,
	timeoutMs: number = 60000,
): Promise<void> {
	const startTime = Date.now();
	const url = `http://${container.getHost()}:${container.getFirstMappedPort()}${endpoint}`;
	const retryIntervalMs = 1000;

	while (Date.now() - startTime < timeoutMs) {
		try {
			const response = await fetch(url);
			if (response.status === 200) {
				return;
			}
		} catch {
			// Don't log errors, just retry
		}

		await wait(retryIntervalMs);
	}

	console.error(
		`WARNING: HTTP endpoint at ${url} did not return 200 within ${
			timeoutMs / 1000
		} seconds. Proceeding with caution.`,
	);
}
