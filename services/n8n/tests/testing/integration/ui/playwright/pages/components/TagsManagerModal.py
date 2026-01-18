"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/components/TagsManagerModal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/components 的组件。导入/依赖:外部:@playwright/test；内部:无；本地:../BasePage。导出:TagsManagerModal。关键函数/方法:getModal、getTable、getTagInputInModal、getFirstTagRow、getDeleteTagButton、getDeleteTagConfirmButton、getDeleteConfirmationMessage、clickAddNewButton、clickCreateTagButton、addTag 等1项。用于渲染该模块UI组件并处理交互/状态。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/components/TagsManagerModal.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/components/TagsManagerModal.py

import type { Locator } from '@playwright/test';

import { BasePage } from '../BasePage';

/**
 * Tags Manager Modal component for managing workflow tags.
 * Used within CanvasPage as `n8n.canvas.tagsManagerModal.*`
 *
 * @example
 * // Access via canvas page
 * await n8n.canvas.openTagManagerModal();
 * await n8n.canvas.tagsManagerModal.clickAddNewButton();
 * await expect(n8n.canvas.tagsManagerModal.getTable()).toBeVisible();
 */
export class TagsManagerModal extends BasePage {
	constructor(private root: Locator) {
		super(root.page());
	}

	getModal(): Locator {
		return this.root;
	}

	getTable(): Locator {
		return this.root.getByTestId('tags-table');
	}

	getTagInputInModal(): Locator {
		return this.getTable().locator('input').first();
	}

	getFirstTagRow(): Locator {
		return this.getTable().locator('tbody tr').first();
	}

	getDeleteTagButton(): Locator {
		return this.root.getByTestId('delete-tag-button');
	}

	getDeleteTagConfirmButton(): Locator {
		return this.root.getByText('Delete tag', { exact: true });
	}

	getDeleteConfirmationMessage(): Locator {
		return this.root.getByText('Are you sure you want to delete this tag?');
	}

	async clickAddNewButton(): Promise<void> {
		await this.root.getByRole('button', { name: 'Add new' }).click();
	}

	async clickCreateTagButton(): Promise<void> {
		await this.root.getByRole('button', { name: 'Create a tag' }).click();
	}

	/**
	 * Start adding a new tag, handling both empty state ("Create a tag") and existing tags ("Add new")
	 */
	async addTag(): Promise<void> {
		const addNewButton = this.root.getByRole('button', { name: 'Add new' });
		const createTagButton = this.root.getByRole('button', { name: 'Create a tag' });
		await addNewButton.or(createTagButton).click();
	}

	async clickDoneButton(): Promise<void> {
		await this.clickButtonByName('Done');
	}
}
