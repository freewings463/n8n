"""
MIGRATION-META:
  source_path: packages/testing/playwright/services/source-control-api-helper.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/services 的服务。导入/依赖:外部:无；内部:无；本地:../Types、./api-helper。导出:SourceControlApiHelper。关键函数/方法:getPreferences、disconnect、connect、pushWorkFolder。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/services/source-control-api-helper.ts -> services/n8n/tests/testing/integration/ui/playwright/services/source_control_api_helper.py

import { TestError } from '../Types';
import type { ApiHelpers } from './api-helper';

export class SourceControlApiHelper {
	constructor(private api: ApiHelpers) {}

	async getPreferences() {
		const response = await this.api.request.get('/rest/source-control/preferences');
		if (!response.ok()) {
			throw new TestError(`Failed to get source control preferences: ${await response.text()}`);
		}
		const result = await response.json();
		return result.data;
	}

	async disconnect({ keepKeyPair = true }: { keepKeyPair?: boolean } = {}) {
		const response = await this.api.request.post('/rest/source-control/disconnect', {
			data: {
				keepKeyPair,
			},
		});
		if (!response.ok()) {
			throw new TestError(`Failed to disconnect from source control: ${await response.text()}`);
		}
		const result = await response.json();
		return result.data;
	}

	async connect(preferences: {
		repositoryUrl: string;
	}) {
		const response = await this.api.request.post('/rest/source-control/preferences', {
			data: {
				connectionType: 'ssh',
				...preferences,
			},
		});

		if (!response.ok()) {
			throw new TestError(`Failed to connect to source control: ${await response.text()}`);
		}
		const result = await response.json();
		return result.data;
	}

	/**
	 * This will push all the changes
	 * OPTIMIZE: add a fileNames to select what specific changes to push
	 * @returns
	 */
	async pushWorkFolder({
		commitMessage,
		force = false,
	}: {
		commitMessage: string;
		force?: boolean;
	}) {
		const response = await this.api.request.post('/rest/source-control/push-workfolder', {
			data: {
				commitMessage,
				force,
				fileNames: [],
			},
		});

		if (!response.ok()) {
			throw new TestError(`Failed to push work folder: ${await response.text()}`);
		}
		const result = await response.json();
		return result.data;
	}
}
