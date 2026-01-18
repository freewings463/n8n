"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/src/n8n-api-client/workflows-api-client.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/src/n8n-api-client 的工作流模块。导入/依赖:外部:无；内部:@/n8n-api-client/n8n-api-client.types；本地:./authenticated-n8n-api-client。导出:WorkflowApiClient。关键函数/方法:getAllWorkflows、createWorkflow、activateWorkflow、archiveWorkflow、deleteWorkflow。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark n8n API client -> infrastructure/external_services/clients
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/src/n8n-api-client/workflows-api-client.ts -> services/n8n/infrastructure/n8n-benchmark/external_services/clients/n8n_api_client/workflows_api_client.py

import type { Workflow } from '@/n8n-api-client/n8n-api-client.types';

import type { AuthenticatedN8nApiClient } from './authenticated-n8n-api-client';

export class WorkflowApiClient {
	constructor(private readonly apiClient: AuthenticatedN8nApiClient) {}

	async getAllWorkflows(): Promise<Workflow[]> {
		const response = await this.apiClient.get<{ count: number; data: Workflow[] }>('/workflows');

		return response.data.data;
	}

	async createWorkflow(workflow: unknown): Promise<Workflow> {
		const response = await this.apiClient.post<{ data: Workflow }>('/workflows', workflow);

		return response.data.data;
	}

	async activateWorkflow(workflow: Workflow): Promise<Workflow> {
		const response = await this.apiClient.post<{ data: Workflow }>(
			`/workflows/${workflow.id}/activate`,
			{
				versionId: workflow.versionId,
			},
		);

		return response.data.data;
	}

	async archiveWorkflow(workflowId: Workflow['id']): Promise<void> {
		await this.apiClient.post(`/workflows/${workflowId}/archive`, {});
	}

	async deleteWorkflow(workflowId: Workflow['id']): Promise<void> {
		await this.apiClient.delete(`/workflows/${workflowId}`);
	}
}
