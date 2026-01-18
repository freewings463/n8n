"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/CredentialsPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:无；内部:无；本地:./BasePage、./components/AddResource、./components/CredentialModal、./components/ResourceCards。导出:CredentialsPage。关键函数/方法:createCredentialFromCredentialPicker、clearSearch、sortByNameDescending、sortByNameAscending、selectCredentialType。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/CredentialsPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/CredentialsPage.py

import { BasePage } from './BasePage';
import { AddResource } from './components/AddResource';
import { CredentialModal } from './components/CredentialModal';
import { ResourceCards } from './components/ResourceCards';

export class CredentialsPage extends BasePage {
	readonly credentialModal = new CredentialModal(this.page.getByTestId('editCredential-modal'));
	readonly addResource = new AddResource(this.page);
	readonly cards = new ResourceCards(this.page);

	get emptyListCreateCredentialButton() {
		return this.page.getByRole('button', { name: 'Add first credential' });
	}

	get createCredentialButton() {
		return this.page.getByTestId('create-credential-button');
	}

	/**
	 * Create a credential from the credentials list, fill fields, save, and close the modal.
	 * @param credentialType - The type of credential to create (e.g. 'Notion API')
	 * @param fields - Key-value pairs for credential fields to fill
	 */
	async createCredentialFromCredentialPicker(
		credentialType: string,
		fields: Record<string, string>,
		options?: { closeDialog?: boolean; name?: string },
	): Promise<void> {
		await this.page.getByRole('combobox', { name: 'Search for app...' }).fill(credentialType);
		await this.page
			.getByTestId('new-credential-type-select-option')
			.filter({ hasText: credentialType })
			.click();
		await this.page.getByTestId('new-credential-type-button').click();
		await this.credentialModal.addCredential(fields, {
			name: options?.name,
			closeDialog: options?.closeDialog,
		});
	}

	async clearSearch() {
		await this.page.getByTestId('resources-list-search').clear();
	}

	async sortByNameDescending() {
		await this.page.getByTestId('resources-list-sort').click();
		await this.page.getByText('Name (Z-A)').click();
	}

	async sortByNameAscending() {
		await this.page.getByTestId('resources-list-sort').click();
		await this.page.getByText('Name (A-Z)').click();
	}

	/**
	 * Select credential type without auto-saving (for tests that need to handle save manually)
	 */
	async selectCredentialType(credentialType: string): Promise<void> {
		await this.page.getByRole('combobox', { name: 'Search for app...' }).fill(credentialType);
		await this.page
			.getByTestId('new-credential-type-select-option')
			.filter({ hasText: credentialType })
			.click();
		await this.page.getByTestId('new-credential-type-button').click();
	}
}
