"""
MIGRATION-META:
  source_path: packages/testing/playwright/services/role-api-helper.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/services 的服务。导入/依赖:外部:nanoid；内部:无；本地:./api-helper、../Types。导出:RoleApiHelper。关键函数/方法:createCustomRole、deleteRole。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/services/role-api-helper.ts -> services/n8n/tests/testing/integration/ui/playwright/services/role_api_helper.py

import { nanoid } from 'nanoid';

import type { ApiHelpers } from './api-helper';
import { TestError } from '../Types';

export class RoleApiHelper {
	constructor(private api: ApiHelpers) {}

	/**
	 * Create a custom role with unique name via REST API
	 * @param scopes Array of scope strings (e.g., ['project:read', 'workflow:read'])
	 * @param displayName Base display name for the role (will be made unique with nanoid)
	 * @returns The created role data including slug
	 */
	async createCustomRole(scopes: string[], displayName: string): Promise<{ slug: string }> {
		const uniqueName = `${displayName} (${nanoid(8)})`;
		const response = await this.api.request.post('/rest/roles', {
			data: {
				displayName: uniqueName,
				description: `Custom role with scopes: ${scopes.join(', ')}`,
				roleType: 'project',
				scopes,
			},
		});

		if (!response.ok()) {
			throw new TestError(`Failed to create custom role: ${await response.text()}`);
		}

		const result = await response.json();
		return result.data;
	}

	/**
	 * Delete a custom role by slug
	 * @param slug The role slug to delete
	 * @returns True if deletion was successful
	 */
	async deleteRole(slug: string): Promise<boolean> {
		const response = await this.api.request.delete(`/rest/roles/${slug}`);

		if (!response.ok()) {
			throw new TestError(`Failed to delete role: ${await response.text()}`);
		}

		return true;
	}
}
