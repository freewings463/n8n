"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/nodes/EditFieldsNode.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/nodes 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:../BasePage。导出:EditFieldsNode。关键函数/方法:setFieldsValues、setSingleFieldValue、ensureFieldExists、setFieldName、setFieldType、setFieldValue、getTypeOptionText、setTextValue、setBooleanValue。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/nodes/EditFieldsNode.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/nodes/EditFieldsNode.py

import type { Locator, Page } from '@playwright/test';

import { BasePage } from '../BasePage';

export class EditFieldsNode extends BasePage {
	constructor(page: Page) {
		super(page);
	}

	async setFieldsValues(
		fields: Array<{
			name: string;
			type: 'string' | 'number' | 'boolean' | 'array' | 'object';
			value: string | number | boolean;
		}>,
		paramName = 'assignments',
	): Promise<void> {
		const container = this.page.getByTestId(`assignment-collection-${paramName}`);

		for (let i = 0; i < fields.length; i++) {
			await this.ensureFieldExists(container, i);
			const assignment = container.getByTestId('assignment').nth(i);

			await this.setFieldName(assignment, fields[i].name);
			await this.setFieldType(assignment, fields[i].type);
			await this.setFieldValue(assignment, fields[i].type, fields[i].value);
		}
	}

	async setSingleFieldValue(
		name: string,
		type: 'string' | 'number' | 'boolean' | 'array' | 'object',
		value: string | number | boolean,
		paramName = 'assignments',
	): Promise<void> {
		await this.setFieldsValues([{ name, type, value }], paramName);
	}

	private async ensureFieldExists(container: Locator, index: number): Promise<void> {
		if (index > 0) {
			await container.getByTestId('assignment-collection-drop-area').click();
			await container.getByTestId('assignment').nth(index).waitFor({ state: 'visible' });
		} else {
			const existingFields = await container.getByTestId('assignment').count();
			if (existingFields === 0) {
				await container.getByTestId('assignment-collection-drop-area').click();
				await container.getByTestId('assignment').first().waitFor({ state: 'visible' });
			}
		}
	}

	private async setFieldName(assignment: Locator, name: string): Promise<void> {
		const nameInput = assignment.getByTestId('assignment-name').getByRole('textbox');
		await nameInput.waitFor({ state: 'visible' });
		await nameInput.fill(name);
		await nameInput.blur();
	}

	private async setFieldType(assignment: Locator, type: string): Promise<void> {
		const typeSelect = assignment.getByTestId('assignment-type-select');
		await typeSelect.waitFor({ state: 'visible' });
		await typeSelect.click();

		const typeOptionText = this.getTypeOptionText(type);
		const option = this.page.getByRole('option', { name: typeOptionText });
		await option.waitFor({ state: 'visible' });
		await option.click();
	}

	private async setFieldValue(
		assignment: Locator,
		type: string,
		value: string | number | boolean,
	): Promise<void> {
		const valueContainer = assignment.getByTestId('assignment-value');
		await valueContainer.waitFor({ state: 'visible' });

		if (type === 'boolean') {
			await this.setBooleanValue(valueContainer, value as boolean);
		} else {
			await this.setTextValue(valueContainer, String(value));
		}
	}

	private getTypeOptionText(type: string): string {
		const typeMap = new Map([
			['string', 'String'],
			['number', 'Number'],
			['boolean', 'Boolean'],
			['array', 'Array'],
			['object', 'Object'],
		]);
		return typeMap.get(type) ?? 'String';
	}

	private async setTextValue(valueContainer: Locator, value: string): Promise<void> {
		const input = valueContainer
			.getByRole('textbox')
			.or(valueContainer.locator('input, textarea, [contenteditable]').first());
		await input.waitFor({ state: 'visible' });
		await input.fill(value);
	}

	private async setBooleanValue(valueContainer: Locator, value: boolean): Promise<void> {
		await valueContainer.click();
		const booleanValue = value ? 'True' : 'False';
		const option = this.page.getByRole('option', { name: booleanValue });
		await option.waitFor({ state: 'visible' });
		await option.click();
	}
}
