"""
MIGRATION-META:
  source_path: packages/testing/playwright/helpers/ClipboardHelper.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/helpers 的模块。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:ClipboardHelper。关键函数/方法:grant、writeText、paste、readText。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/helpers/ClipboardHelper.ts -> services/n8n/tests/testing/integration/ui/playwright/helpers/ClipboardHelper.py

import type { Page } from '@playwright/test';

export class ClipboardHelper {
	constructor(private readonly page: Page) {}

	/**
	 * Grant clipboard permissions
	 * @param mode - Permission mode: 'read', 'write', or 'readwrite' (default)
	 */
	async grant(mode: 'read' | 'write' | 'readwrite' = 'readwrite'): Promise<void> {
		let permissions = ['clipboard-read', 'clipboard-write'];

		if (mode === 'read') {
			permissions = ['clipboard-read'];
		} else if (mode === 'write') {
			permissions = ['clipboard-write'];
		}

		await this.page.context().grantPermissions(permissions);
	}

	/**
	 * Write text to clipboard using page.evaluate.
	 * @param text - The text to write to clipboard
	 */
	async writeText(text: string): Promise<void> {
		await this.page.evaluate(async (data) => {
			await navigator.clipboard.writeText(data);
		}, text);
	}

	/**
	 * Write text to clipboard and simulate paste keyboard action.
	 * @param text - The text to write to clipboard and paste
	 */
	async paste(text: string): Promise<void> {
		await this.grant();
		await this.writeText(text);
		await this.page.keyboard.press('ControlOrMeta+V');
	}

	/**
	 * Read text from clipboard using page.evaluate.
	 * @returns The text from clipboard
	 */
	async readText(): Promise<string> {
		return await this.page.evaluate(() => navigator.clipboard.readText());
	}
}
