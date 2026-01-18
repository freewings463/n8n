"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/src/n8n-api-client/credentials-api-client.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/src/n8n-api-client 的模块。导入/依赖:外部:无；内部:@/n8n-api-client/n8n-api-client.types；本地:./authenticated-n8n-api-client。导出:CredentialApiClient。关键函数/方法:getAllCredentials、createCredential、deleteCredential。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark n8n API client -> infrastructure/external_services/clients
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/src/n8n-api-client/credentials-api-client.ts -> services/n8n/infrastructure/n8n-benchmark/external_services/clients/n8n_api_client/credentials_api_client.py

import type { Credential } from '@/n8n-api-client/n8n-api-client.types';

import type { AuthenticatedN8nApiClient } from './authenticated-n8n-api-client';

export class CredentialApiClient {
	constructor(private readonly apiClient: AuthenticatedN8nApiClient) {}

	async getAllCredentials(): Promise<Credential[]> {
		const response = await this.apiClient.get<{ count: number; data: Credential[] }>(
			'/credentials',
		);

		return response.data.data;
	}

	async createCredential(credential: Credential): Promise<Credential> {
		const response = await this.apiClient.post<{ data: Credential }>('/credentials', {
			...credential,
			id: undefined,
		});

		return response.data.data;
	}

	async deleteCredential(credentialId: Credential['id']): Promise<void> {
		await this.apiClient.delete(`/credentials/${credentialId}`);
	}
}
