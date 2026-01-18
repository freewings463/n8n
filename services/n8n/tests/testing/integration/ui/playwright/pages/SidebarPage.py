"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/SidebarPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:SidebarPage。关键函数/方法:clickAddProjectButton、clickHomeButton、universalAdd、clickHomeMenuItem、clickPersonalMenuItem、clickWorkflowsLink、clickCredentialsLink、addProjectFromUniversalAdd、getProjectButtonInUniversalAdd、addWorkflowFromUniversalAdd 等25项。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/SidebarPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/SidebarPage.py

import { expect, type Locator, type Page } from '@playwright/test';

export class SidebarPage {
	readonly page: Page;

	constructor(page: Page) {
		this.page = page;
	}

	async clickAddProjectButton() {
		await this.page.getByTestId('project-plus-button').click();
	}

	async clickHomeButton() {
		await this.page.getByTestId('project-home-menu-item').click();
	}

	async universalAdd() {
		await this.page.getByTestId('universal-add').click();
	}

	async clickHomeMenuItem() {
		await this.page.getByTestId('project-home-menu-item').click();
	}

	async clickPersonalMenuItem() {
		await this.page.getByTestId('project-personal-menu-item').click();
	}

	async clickWorkflowsLink(): Promise<void> {
		await this.page.getByRole('link', { name: 'Workflows' }).click();
	}

	async clickCredentialsLink(): Promise<void> {
		await this.page.getByRole('link', { name: 'Credentials' }).click();
	}

	async addProjectFromUniversalAdd() {
		await this.universalAdd();
		await this.page.getByTestId('navigation-menu-item').filter({ hasText: 'Project' }).click();
	}

	getProjectButtonInUniversalAdd(): Locator {
		return this.page.getByTestId('navigation-menu-item').filter({ hasText: 'Project' });
	}

	async addWorkflowFromUniversalAdd(projectName: string) {
		await this.universalAdd();
		await this.page.getByTestId('universal-add').getByText('Workflow').click();
		await this.page.getByTestId('universal-add').getByRole('link', { name: projectName }).click();
	}

	async openNewCredentialDialogForProject(projectName: string) {
		await this.universalAdd();
		await this.page.getByTestId('universal-add').getByText('Credential', { exact: true }).click();
		await this.page.getByTestId('universal-add').getByRole('link', { name: projectName }).click();
	}

	getProjectMenuItems(): Locator {
		return this.page.getByTestId('project-menu-item');
	}

	async clickProjectMenuItem(projectName: string) {
		await this.expand();
		await this.getProjectMenuItems().filter({ hasText: projectName }).click();
	}

	getAddFirstProjectButton(): Locator {
		return this.page.getByTestId('add-first-project-button');
	}

	getSettings(): Locator {
		return this.page.getByTestId('main-sidebar-settings');
	}

	getLogoutMenuItem(): Locator {
		return this.page.getByTestId('main-sidebar-log-out');
	}

	getAboutModal(): Locator {
		return this.page.getByTestId('about-modal');
	}

	getHelp(): Locator {
		return this.page.getByTestId('main-sidebar-help');
	}

	async clickHelpMenuItem(): Promise<void> {
		await this.getHelp().click();
	}

	async clickAboutMenuItem(): Promise<void> {
		await this.getHelp().click();
		await this.page.getByTestId('about').click();
	}

	async openAboutModalViaShortcut(): Promise<void> {
		await this.page.keyboard.press('Alt+Meta+o');
	}

	async closeAboutModal(): Promise<void> {
		await this.page.getByTestId('close-about-modal-button').click();
	}

	getAdminPanel(): Locator {
		return this.page.getByTestId('main-sidebar-cloud-admin');
	}

	getTrialBanner(): Locator {
		return this.page.getByTestId('banners-TRIAL');
	}

	getMainSidebarTrialUpgrade(): Locator {
		return this.page.getByTestId('main-sidebar-trial-upgrade');
	}

	getTemplatesLink(): Locator {
		return this.page.getByTestId('main-sidebar-templates').locator('a');
	}

	getVersionUpdateItem(): Locator {
		return this.page.getByTestId('version-update-cta-button');
	}

	getSourceControlPushButton(): Locator {
		return this.page.getByTestId('main-sidebar-source-control-push');
	}

	getSourceControlPullButton(): Locator {
		return this.page.getByTestId('main-sidebar-source-control-pull');
	}

	getSourceControlConnectedIndicator(): Locator {
		return this.page.getByTestId('main-sidebar-source-control-connected');
	}

	async openSettings(): Promise<void> {
		await this.getSettings().click();
	}

	async clickSignout(): Promise<void> {
		await this.expand();
		await this.openSettings();
		await this.getLogoutMenuItem().click();
	}

	async signOutFromWorkflows(): Promise<void> {
		await this.page.goto('/workflows');
		await this.clickSignout();
	}

	async goToWorkflows(): Promise<void> {
		await this.page.goto('/workflows');
	}

	async expand() {
		// First ensure the sidebar is visible before checking if it is expanded
		await expect(this.getSettings()).toBeVisible();

		const logo = this.page.getByTestId('n8n-logo');
		const isExpanded = await logo.isVisible();

		if (!isExpanded) {
			const collapseButton = this.page.locator('#toggle-sidebar-button');
			await expect(collapseButton).toBeVisible();
			await collapseButton.click();
		}
	}
}
