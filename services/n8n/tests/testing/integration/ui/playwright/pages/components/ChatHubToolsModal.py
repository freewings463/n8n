"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/components/ChatHubToolsModal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/components 的组件。导入/依赖:外部:@playwright/test；内部:无；本地:无。导出:ChatHubToolsModal。关键函数/方法:getRoot、getProviderSection、getCredentialSelect、getToolSwitch、getConfirmButton。用于渲染该模块UI组件并处理交互/状态。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/components/ChatHubToolsModal.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/components/ChatHubToolsModal.py

import type { Locator } from '@playwright/test';

export class ChatHubToolsModal {
	constructor(private root: Locator) {}

	getRoot(): Locator {
		return this.root;
	}

	getProviderSection(providerName: string): Locator {
		return this.root.locator('[class*="provider"]').filter({ hasText: providerName });
	}

	getCredentialSelect(providerName: string): Locator {
		return this.getProviderSection(providerName).getByRole('combobox');
	}

	getToolSwitch(providerName: string, toolName: string): Locator {
		return this.getProviderSection(providerName).getByLabel(`Toggle ${toolName}`);
	}

	getConfirmButton(): Locator {
		return this.root.getByRole('button', { name: 'Confirm' });
	}
}
