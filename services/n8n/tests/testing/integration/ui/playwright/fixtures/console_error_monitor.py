"""
MIGRATION-META:
  source_path: packages/testing/playwright/fixtures/console-error-monitor.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/fixtures 的模块。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:consoleErrorFixtures。关键函数/方法:attach、detach、hasErrors、getErrors、async。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/fixtures/console-error-monitor.ts -> services/n8n/tests/testing/integration/ui/playwright/fixtures/console_error_monitor.py

import type { BrowserContext, ConsoleMessage, TestInfo } from '@playwright/test';

interface ConsoleError {
	type: string;
	text: string;
	location: string;
	timestamp: number;
}

/**
 * Monitors browser context for console errors.
 * Attaches diagnostic info to test results when errors occur.
 * No-op when no errors are detected.
 */
class ConsoleErrorMonitor {
	private errors: ConsoleError[] = [];

	private readonly listener = (message: ConsoleMessage) => {
		if (message.type() === 'error') {
			this.errors.push({
				type: message.type(),
				text: message.text(),
				location: message.location().url,
				timestamp: Date.now(),
			});
		}
	};

	attach(context: BrowserContext): void {
		context.on('console', this.listener);
	}

	detach(context: BrowserContext): void {
		context.off('console', this.listener);
	}

	hasErrors(): boolean {
		return this.errors.length > 0;
	}

	getErrors(): ConsoleError[] {
		return this.errors;
	}
}

/**
 * Console error monitor fixtures for capturing browser errors.
 * Spread into test.extend() to enable monitoring.
 */
export const consoleErrorFixtures = {
	_consoleErrorMonitor: [
		async (
			{ context }: { context: BrowserContext },
			use: (monitor: ConsoleErrorMonitor) => Promise<void>,
			testInfo: TestInfo,
		) => {
			const monitor = new ConsoleErrorMonitor();
			monitor.attach(context);

			await use(monitor);

			monitor.detach(context);

			// Attach diagnostics if errors occurred
			if (monitor.hasErrors()) {
				await testInfo.attach('console-errors', {
					body: JSON.stringify(
						{
							errors: monitor.getErrors(),
							testTitle: testInfo.title,
							project: testInfo.project.name,
						},
						null,
						2,
					),
					contentType: 'application/json',
				});
			}
		},
		{ auto: true },
	],
};
