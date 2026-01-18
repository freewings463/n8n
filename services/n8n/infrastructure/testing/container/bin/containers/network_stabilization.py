"""
MIGRATION-META:
  source_path: packages/testing/containers/network-stabilization.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/containers 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:waitForNetworkQuiet、cleanup、resolve。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected child_process execution -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/containers/network-stabilization.ts -> services/n8n/infrastructure/testing/container/bin/containers/network_stabilization.py

import { spawn } from 'child_process';
import os from 'os';

/**
 * Wait for the Linux network stack to become quiet (no netlink events).
 * This monitors actual kernel network events rather than guessing with fixed delays.
 *
 * Only runs in CI on Linux. On other platforms or local dev, resolves immediately.
 *
 * @param quietDurationMs - How long the network must be quiet before resolving (default: 2000ms)
 * @param maxWaitMs - Maximum time to wait before giving up (default: 10000ms)
 */
export async function waitForNetworkQuiet(
	quietDurationMs = 2000,
	maxWaitMs = 10000,
): Promise<void> {
	// Only run in CI on Linux
	if (!process.env.CI || os.platform() !== 'linux') {
		return;
	}

	return await new Promise((resolve) => {
		let lastEventTime = Date.now();
		let checkInterval: NodeJS.Timeout | null = null;
		let maxTimeout: NodeJS.Timeout | null = null;
		let resolved = false;

		const cleanup = () => {
			if (resolved) return;
			resolved = true;
			if (checkInterval) clearInterval(checkInterval);
			if (maxTimeout) clearTimeout(maxTimeout);
			monitor.kill();
		};

		// Monitor network events using `ip monitor`
		// Watches: link (interfaces), address (IP assignments), route (routing table)
		const monitor = spawn('ip', ['monitor', 'link', 'address', 'route'], {
			stdio: ['ignore', 'pipe', 'pipe'],
		});

		monitor.on('error', (error: Error) => {
			// ip command not available - fall back to no-op
			console.warn(`[network-stabilization] ip monitor not available: ${error.message}`);
			cleanup();
			resolve();
		});

		monitor.stdout.on('data', () => {
			// Network change detected, reset timer
			lastEventTime = Date.now();
		});

		monitor.stderr.on('data', (data) => {
			console.warn(`[network-stabilization] ip monitor stderr: ${data}`);
		});

		// Check periodically if network has been quiet long enough
		checkInterval = setInterval(() => {
			const quietDuration = Date.now() - lastEventTime;
			if (quietDuration >= quietDurationMs) {
				console.log(`[network-stabilization] Network quiet for ${quietDuration}ms, proceeding`);
				cleanup();
				resolve();
			}
		}, 100);

		// Maximum wait timeout
		maxTimeout = setTimeout(() => {
			console.warn(`[network-stabilization] Max wait (${maxWaitMs}ms) exceeded, proceeding anyway`);
			cleanup();
			resolve();
		}, maxWaitMs);

		// Handle process exit
		monitor.on('close', () => {
			if (!resolved) {
				cleanup();
				resolve();
			}
		});
	});
}
