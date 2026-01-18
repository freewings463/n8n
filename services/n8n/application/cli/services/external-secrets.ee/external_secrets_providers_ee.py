"""
MIGRATION-META:
  source_path: packages/cli/src/modules/external-secrets.ee/external-secrets-providers.ee.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/external-secrets.ee 的模块。导入/依赖:外部:无；内部:@n8n/di；本地:./providers/aws-secrets-manager、../azure-key-vault/azure-key-vault、../gcp-secrets-manager/gcp-secrets-manager、./providers/infisical 等2项。导出:ExternalSecretsProviders。关键函数/方法:getProvider、hasProvider、getAllProviders。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/external-secrets.ee/external-secrets-providers.ee.ts -> services/n8n/application/cli/services/external-secrets.ee/external_secrets_providers_ee.py

import { Service } from '@n8n/di';

import { AwsSecretsManager } from './providers/aws-secrets-manager';
import { AzureKeyVault } from './providers/azure-key-vault/azure-key-vault';
import { GcpSecretsManager } from './providers/gcp-secrets-manager/gcp-secrets-manager';
import { InfisicalProvider } from './providers/infisical';
import { VaultProvider } from './providers/vault';
import type { SecretsProvider } from './types';

@Service()
export class ExternalSecretsProviders {
	providers: Record<string, { new (): SecretsProvider }> = {
		awsSecretsManager: AwsSecretsManager,
		infisical: InfisicalProvider,
		vault: VaultProvider,
		azureKeyVault: AzureKeyVault,
		gcpSecretsManager: GcpSecretsManager,
	};

	getProvider(name: string): { new (): SecretsProvider } {
		return this.providers[name];
	}

	hasProvider(name: string) {
		return name in this.providers;
	}

	getAllProviders() {
		return this.providers;
	}
}
