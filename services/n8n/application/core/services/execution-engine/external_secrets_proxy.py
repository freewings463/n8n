"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/external-secrets-proxy.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine 的执行模块。导入/依赖:外部:无；内部:@n8n/di；本地:无。导出:IExternalSecretsManager、ExternalSecretsProxy。关键函数/方法:update、updateSecrets、hasSecret、getSecret、getSecretNames、hasProvider、getProviderNames、setManager、listProviders、listSecrets。用于承载执行实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/external-secrets-proxy.ts -> services/n8n/application/core/services/execution-engine/external_secrets_proxy.py

import { Service } from '@n8n/di';

export interface IExternalSecretsManager {
	updateSecrets(): Promise<void>;
	hasSecret(provider: string, name: string): boolean;
	getSecret(provider: string, name: string): unknown;
	getSecretNames(provider: string): string[];
	hasProvider(provider: string): boolean;
	getProviderNames(): string[];
}

@Service()
export class ExternalSecretsProxy {
	private manager?: IExternalSecretsManager;

	setManager(manager: IExternalSecretsManager) {
		this.manager = manager;
	}

	async update() {
		await this.manager?.updateSecrets();
	}

	getSecret(provider: string, name: string) {
		return this.manager?.getSecret(provider, name);
	}

	hasSecret(provider: string, name: string): boolean {
		return !!this.manager && this.manager.hasSecret(provider, name);
	}

	hasProvider(provider: string): boolean {
		return !!this.manager && this.manager.hasProvider(provider);
	}

	listProviders(): string[] {
		return this.manager?.getProviderNames() ?? [];
	}

	listSecrets(provider: string): string[] {
		return this.manager?.getSecretNames(provider) ?? [];
	}
}
