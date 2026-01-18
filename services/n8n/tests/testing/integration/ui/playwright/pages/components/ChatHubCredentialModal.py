"""
MIGRATION-META:
  source_path: packages/testing/playwright/pages/components/ChatHubCredentialModal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/pages/components 的组件。导入/依赖:外部:@playwright/test；内部:无；本地:./BaseModal。导出:ChatHubCredentialModal。关键函数/方法:getRoot、getCredentialSelector、getCreateButton。用于渲染该模块UI组件并处理交互/状态。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/pages/components/ChatHubCredentialModal.ts -> services/n8n/tests/testing/integration/ui/playwright/pages/components/ChatHubCredentialModal.py

import type { Locator } from '@playwright/test';

import { BaseModal } from './BaseModal';

export class ChatHubCredentialModal extends BaseModal {
	constructor(private root: Locator) {
		super(root.page());
	}

	getRoot(): Locator {
		return this.root;
	}

	getCredentialSelector(): Locator {
		return this.root.getByRole('combobox');
	}

	getCreateButton(): Locator {
		return this.page.getByTestId('node-credentials-select-item-new');
	}
}
