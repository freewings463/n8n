"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/NpsSurveyPage.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages 的页面。导入/依赖:外部:@playwright/test；内部:无；本地:./BasePage。导出:NpsSurveyPage。关键函数/方法:getNpsSurveyModal、getNpsSurveyRatings、getNpsSurveyFeedback、getNpsSurveySubmitButton、getNpsSurveyCloseButton、getRatingButton、getFeedbackTextarea、clickRating、fillFeedback、clickSubmitButton 等2项。用于组装该模块页面级逻辑与子组件。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/NpsSurveyPage.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/NpsSurveyPage.py

import type { Locator, Page } from '@playwright/test';

import { BasePage } from './BasePage';

export class NpsSurveyPage extends BasePage {
	constructor(page: Page) {
		super(page);
	}

	getNpsSurveyModal(): Locator {
		return this.page.getByTestId('nps-survey-modal');
	}

	getNpsSurveyRatings(): Locator {
		return this.page.getByTestId('nps-survey-ratings');
	}

	getNpsSurveyFeedback(): Locator {
		return this.page.getByTestId('nps-survey-feedback');
	}

	getNpsSurveySubmitButton(): Locator {
		return this.page.getByTestId('nps-survey-feedback-button');
	}

	getNpsSurveyCloseButton(): Locator {
		return this.getNpsSurveyModal().locator('button.el-drawer__close-btn');
	}

	getRatingButton(rating: number): Locator {
		return this.getNpsSurveyRatings().locator('button').nth(rating);
	}

	getFeedbackTextarea(): Locator {
		return this.getNpsSurveyFeedback().locator('textarea');
	}

	async clickRating(rating: number): Promise<void> {
		await this.getRatingButton(rating).click();
	}

	async fillFeedback(feedback: string): Promise<void> {
		await this.getFeedbackTextarea().fill(feedback);
	}

	async clickSubmitButton(): Promise<void> {
		await this.getNpsSurveySubmitButton().click();
	}

	async closeSurvey(): Promise<void> {
		await this.getNpsSurveyCloseButton().click();
	}

	async getRatingButtonCount(): Promise<number> {
		return await this.getNpsSurveyRatings().locator('button').count();
	}
}
