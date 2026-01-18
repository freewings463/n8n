"""
MIGRATION-META:
  source_path: packages/testing/playwright/composables/ProjectComposer.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/composables 的组合式函数。导入/依赖:外部:nanoid；内部:无；本地:../pages/n8nPage。导出:ProjectComposer。关键函数/方法:createProject、addCredentialToProject、extractIdFromUrl、extractProjectIdFromPage。用于封装该模块复用逻辑（hooks/composables）供组件组合。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/composables/ProjectComposer.ts -> services/n8n/tests/testing/integration/ui/playwright/composables/ProjectComposer.py

import { nanoid } from 'nanoid';

import type { n8nPage } from '../pages/n8nPage';

export class ProjectComposer {
	constructor(private readonly n8n: n8nPage) {}

	/**
	 * Create a project and return the project name and ID. If no project name is provided, a unique name will be generated.
	 * @param projectName - The name of the project to create.
	 * @returns The project name and ID.
	 */
	async createProject(projectName?: string) {
		await this.n8n.page.getByTestId('universal-add').click();
		await this.n8n.page.getByTestId('navigation-menu-item').filter({ hasText: 'Project' }).click();
		await this.n8n.notifications.waitForNotificationAndClose('saved successfully');
		await this.n8n.page.waitForLoadState();
		const projectNameUnique = projectName ?? `Project ${nanoid(8)}`;
		await this.n8n.projectSettings.fillProjectName(projectNameUnique);
		await this.n8n.projectSettings.clickSaveButton();
		const projectId = this.extractProjectIdFromPage('projects', 'settings');
		return { projectName: projectNameUnique, projectId };
	}

	/**
	 * Add a new credential to a project.
	 * @param projectName - The name of the project to add the credential to.
	 * @param credentialType - The type of credential to add by visible name e.g 'Notion API'
	 * @param credentialFieldName - The name of the field to add the credential to. e.g. 'apiKey' which would be data-test-id='parameter-input-apiKey'
	 * @param credentialValue - The value of the credential to add.
	 */
	async addCredentialToProject(
		projectName: string,
		credentialType: string,
		credentialFieldName: string,
		credentialValue: string,
	) {
		await this.n8n.sideBar.openNewCredentialDialogForProject(projectName);
		await this.n8n.credentials.createCredentialFromCredentialPicker(credentialType, {
			[credentialFieldName]: credentialValue,
		});
	}

	extractIdFromUrl(url: string, beforeWord: string, afterWord: string): string {
		const path = url.includes('://') ? new URL(url).pathname : url;
		const match = path.match(new RegExp(`/${beforeWord}/([^/]+)/${afterWord}`));
		return match?.[1] ?? '';
	}

	extractProjectIdFromPage(beforeWord: string, afterWord: string): string {
		return this.extractIdFromUrl(this.n8n.page.url(), beforeWord, afterWord);
	}
}
