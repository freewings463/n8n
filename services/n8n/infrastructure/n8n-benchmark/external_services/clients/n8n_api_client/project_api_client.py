"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/src/n8n-api-client/project-api-client.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/src/n8n-api-client 的模块。导入/依赖:外部:无；内部:无；本地:./authenticated-n8n-api-client。导出:ProjectApiClient。关键函数/方法:getPersonalProject。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark n8n API client -> infrastructure/external_services/clients
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/src/n8n-api-client/project-api-client.ts -> services/n8n/infrastructure/n8n-benchmark/external_services/clients/n8n_api_client/project_api_client.py

import type { AuthenticatedN8nApiClient } from './authenticated-n8n-api-client';

export class ProjectApiClient {
	constructor(private readonly apiClient: AuthenticatedN8nApiClient) {}

	async getPersonalProject(): Promise<string> {
		const response = await this.apiClient.get<{ data: { id: string } }>('/projects/personal');

		return response.data.data.id;
	}
}
