"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/src/n8n-api-client/n8n-api-client.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/src/n8n-api-client 的模块。导入/依赖:外部:axios；内部:无；本地:无。导出:N8nApiClient。关键函数/方法:waitForInstanceToBecomeOnline、setupOwnerIfNeeded、delay、getRestEndpointUrl。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected external HTTP client usage -> infrastructure/external_services/clients
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/src/n8n-api-client/n8n-api-client.ts -> services/n8n/infrastructure/n8n-benchmark/external_services/clients/n8n-api-client/n8n_api_client.py

import type { AxiosError, AxiosRequestConfig } from 'axios';
import axios from 'axios';

export class N8nApiClient {
	constructor(readonly apiBaseUrl: string) {}

	async waitForInstanceToBecomeOnline(): Promise<void> {
		const HEALTH_ENDPOINT = 'healthz';
		const START_TIME = Date.now();
		const INTERVAL_MS = 1000;
		const TIMEOUT_MS = 60_000;

		while (Date.now() - START_TIME < TIMEOUT_MS) {
			try {
				const response = await axios.request<{ status: 'ok' }>({
					url: `${this.apiBaseUrl}/${HEALTH_ENDPOINT}`,
					method: 'GET',
				});

				if (response.status === 200 && response.data.status === 'ok') {
					return;
				}
			} catch {}

			console.log(`n8n instance not online yet, retrying in ${INTERVAL_MS / 1000} seconds...`);
			await this.delay(INTERVAL_MS);
		}

		throw new Error(`n8n instance did not come online within ${TIMEOUT_MS / 1000} seconds`);
	}

	async setupOwnerIfNeeded(loginDetails: { email: string; password: string }) {
		const response = await this.restApiRequest<{ message: string }>('/owner/setup', {
			method: 'POST',
			data: {
				email: loginDetails.email,
				password: loginDetails.password,
				firstName: 'Test',
				lastName: 'User',
			},
			// Don't throw on non-2xx responses
			validateStatus: () => true,
		});

		const responsePayload = response.data;

		if (response.status === 200) {
			console.log('Owner setup successful');
		} else if (response.status === 400) {
			if (responsePayload.message === 'Instance owner already setup')
				console.log('Owner already set up');
		} else if (response.status === 404) {
			// The n8n instance setup owner endpoint not be available yet even tho
			// the health endpoint returns ok. In this case we simply retry.
			console.log('Owner setup endpoint not available yet, retrying in 1s...');
			await this.delay(1000);
			await this.setupOwnerIfNeeded(loginDetails);
		} else {
			throw new Error(
				`Owner setup failed with status ${response.status}: ${responsePayload.message}`,
			);
		}
	}

	async restApiRequest<T>(endpoint: string, init: Omit<AxiosRequestConfig, 'url'>) {
		try {
			return await axios.request<T>({
				...init,
				url: this.getRestEndpointUrl(endpoint),
			});
		} catch (e) {
			const error = e as AxiosError;
			console.error(`[ERROR] Request failed ${init.method} ${endpoint}`, error?.response?.data);
			throw error;
		}
	}

	async delay(ms: number): Promise<void> {
		return await new Promise((resolve) => setTimeout(resolve, ms));
	}

	protected getRestEndpointUrl(endpoint: string) {
		return `${this.apiBaseUrl}/rest${endpoint}`;
	}
}
