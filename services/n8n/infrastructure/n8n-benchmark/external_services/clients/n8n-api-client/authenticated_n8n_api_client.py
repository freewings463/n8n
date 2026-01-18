"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/src/n8n-api-client/authenticated-n8n-api-client.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/src/n8n-api-client 的模块。导入/依赖:外部:axios；内部:无；本地:./n8n-api-client。导出:AuthenticatedN8nApiClient。关键函数/方法:createUsingUsernameAndPassword。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected external HTTP client usage -> infrastructure/external_services/clients
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/src/n8n-api-client/authenticated-n8n-api-client.ts -> services/n8n/infrastructure/n8n-benchmark/external_services/clients/n8n-api-client/authenticated_n8n_api_client.py

import type { AxiosRequestConfig } from 'axios';

import { N8nApiClient } from './n8n-api-client';

export class AuthenticatedN8nApiClient extends N8nApiClient {
	constructor(
		apiBaseUrl: string,
		private readonly authCookie: string,
	) {
		super(apiBaseUrl);
	}

	static async createUsingUsernameAndPassword(
		apiClient: N8nApiClient,
		loginDetails: {
			email: string;
			password: string;
		},
	): Promise<AuthenticatedN8nApiClient> {
		const response = await apiClient.restApiRequest('/login', {
			method: 'POST',
			data: {
				emailOrLdapLoginId: loginDetails.email,
				password: loginDetails.password,
			},
		});

		if (response.data === 'n8n is starting up. Please wait') {
			await apiClient.delay(1000);
			return await this.createUsingUsernameAndPassword(apiClient, loginDetails);
		}

		const cookieHeader = response.headers['set-cookie'];
		const authCookie = Array.isArray(cookieHeader) ? cookieHeader.join('; ') : cookieHeader;
		if (!authCookie) {
			throw new Error(
				'Did not receive authentication cookie even tho login succeeded: ' +
					JSON.stringify(
						{
							status: response.status,
							headers: response.headers,
							data: response.data,
						},
						null,
						2,
					),
			);
		}

		return new AuthenticatedN8nApiClient(apiClient.apiBaseUrl, authCookie);
	}

	async get<T>(endpoint: string) {
		return await this.authenticatedRequest<T>(endpoint, {
			method: 'GET',
		});
	}

	async post<T>(endpoint: string, data: unknown) {
		return await this.authenticatedRequest<T>(endpoint, {
			method: 'POST',
			data,
		});
	}

	async patch<T>(endpoint: string, data: unknown) {
		return await this.authenticatedRequest<T>(endpoint, {
			method: 'PATCH',
			data,
		});
	}

	async delete<T>(endpoint: string) {
		return await this.authenticatedRequest<T>(endpoint, {
			method: 'DELETE',
		});
	}

	protected async authenticatedRequest<T>(endpoint: string, init: Omit<AxiosRequestConfig, 'url'>) {
		return await this.restApiRequest<T>(endpoint, {
			...init,
			headers: {
				...init.headers,
				cookie: this.authCookie,
			},
		});
	}
}
