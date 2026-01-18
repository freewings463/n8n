"""
MIGRATION-META:
  source_path: packages/testing/playwright/services/variables-api-helper.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/services 的服务。导入/依赖:外部:无；内部:无；本地:./api-helper、../Types。导出:VariablesApiHelper。关键函数/方法:createVariable、getAllVariables、getVariable、updateVariable、deleteVariable、deleteAllVariables、createTestVariable、cleanupTestVariables。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/services/variables-api-helper.ts -> services/n8n/tests/testing/integration/ui/playwright/services/variables_api_helper.py

import type { ApiHelpers } from './api-helper';
import { TestError } from '../Types';

interface VariableResponse {
	id: string;
	key: string;
	value: string;
}

interface CreateVariableDto {
	key: string;
	value: string;
	projectId?: string;
}

interface UpdateVariableDto {
	key?: string;
	value?: string;
}

export class VariablesApiHelper {
	constructor(private api: ApiHelpers) {}

	/**
	 * Create a new variable
	 */
	async createVariable(variable: CreateVariableDto): Promise<VariableResponse> {
		const response = await this.api.request.post('/rest/variables', { data: variable });

		if (!response.ok()) {
			throw new TestError(`Failed to create variable: ${await response.text()}`);
		}

		const result = await response.json();
		return result.data ?? result;
	}

	/**
	 * Get all variables
	 */
	async getAllVariables(): Promise<VariableResponse[]> {
		const response = await this.api.request.get('/rest/variables');

		if (!response.ok()) {
			throw new TestError(`Failed to get variables: ${await response.text()}`);
		}

		const result = await response.json();
		return result.data ?? result;
	}

	/**
	 * Get a variable by ID
	 */
	async getVariable(id: string): Promise<VariableResponse> {
		const response = await this.api.request.get(`/rest/variables/${id}`);

		if (!response.ok()) {
			throw new TestError(`Failed to get variable: ${await response.text()}`);
		}

		const result = await response.json();
		return result.data ?? result;
	}

	/**
	 * Update a variable by ID
	 */
	async updateVariable(id: string, updates: UpdateVariableDto): Promise<VariableResponse> {
		const response = await this.api.request.patch(`/rest/variables/${id}`, { data: updates });

		if (!response.ok()) {
			throw new TestError(`Failed to update variable: ${await response.text()}`);
		}

		const result = await response.json();
		return result.data ?? result;
	}

	/**
	 * Delete a variable by ID
	 */
	async deleteVariable(id: string): Promise<void> {
		const response = await this.api.request.delete(`/rest/variables/${id}`);

		if (!response.ok()) {
			throw new TestError(`Failed to delete variable: ${await response.text()}`);
		}
	}

	/**
	 * Delete all variables (useful for test cleanup)
	 */
	async deleteAllVariables(): Promise<void> {
		const variables = await this.getAllVariables();

		// Delete variables in parallel for better performance
		await Promise.all(variables.map((variable) => this.deleteVariable(variable.id)));
	}

	/**
	 * Create a test variable with a unique key
	 */
	async createTestVariable(
		keyPrefix: string = 'TEST_VAR',
		value: string = 'test_value',
		projectId?: string,
	): Promise<VariableResponse> {
		const key = `${keyPrefix}_${Date.now()}_${Math.random().toString(36).slice(2, 11)}`;
		return await this.createVariable({ key, value, projectId });
	}

	/**
	 * Clean up variables by key pattern (useful for test cleanup)
	 */
	async cleanupTestVariables(keyPattern?: string): Promise<void> {
		const variables = await this.getAllVariables();

		const variablesToDelete = keyPattern
			? variables.filter((variable) => variable.key.includes(keyPattern))
			: variables.filter((variable) => variable.key.startsWith('TEST_'));

		await Promise.all(variablesToDelete.map((variable) => this.deleteVariable(variable.id)));
	}
}
