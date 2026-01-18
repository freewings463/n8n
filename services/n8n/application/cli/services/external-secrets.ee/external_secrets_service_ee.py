"""
MIGRATION-META:
  source_path: packages/cli/src/modules/external-secrets.ee/external-secrets.service.ee.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/external-secrets.ee 的服务。导入/依赖:外部:无；内部:@n8n/di、n8n-workflow、@/constants；本地:./external-secrets-manager.ee、./types。导出:ExternalSecretsService。关键函数/方法:getProvider、getProviders、redact、unredactRestoreValues、unredact、saveProviderSettings、saveProviderConnected、getAllSecrets、testProviderSettings、updateProvider。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/external-secrets.ee/external-secrets.service.ee.ts -> services/n8n/application/cli/services/external-secrets.ee/external_secrets_service_ee.py

import { Service } from '@n8n/di';
import type { IDataObject } from 'n8n-workflow';
import { deepCopy } from 'n8n-workflow';

import { CREDENTIAL_BLANKING_VALUE } from '@/constants';

import { ExternalSecretsManager } from './external-secrets-manager.ee';
import type { ExternalSecretsRequest, SecretsProvider } from './types';

@Service()
export class ExternalSecretsService {
	constructor(private readonly externalSecretsManager: ExternalSecretsManager) {}

	getProvider(providerName: string): ExternalSecretsRequest.GetProviderResponse | null {
		const providerAndSettings = this.externalSecretsManager.getProviderWithSettings(providerName);
		const { provider, settings } = providerAndSettings;
		return {
			displayName: provider.displayName,
			name: provider.name,
			icon: provider.name,
			state: provider.state,
			connected: settings.connected,
			connectedAt: settings.connectedAt,
			properties: provider.properties,
			data: this.redact(settings.settings, provider),
		};
	}

	getProviders() {
		return this.externalSecretsManager.getProvidersWithSettings().map(({ provider, settings }) => ({
			displayName: provider.displayName,
			name: provider.name,
			icon: provider.name,
			state: provider.state,
			connected: !!settings.connected,
			connectedAt: settings.connectedAt,
			data: this.redact(settings.settings, provider),
		}));
	}

	// Take data and replace all sensitive values with a sentinel value.
	// This will replace password fields and oauth data.
	redact(data: IDataObject, provider: SecretsProvider): IDataObject {
		const copiedData = deepCopy(data || {});

		const properties = provider.properties;

		for (const dataKey of Object.keys(copiedData)) {
			// The frontend only cares that this value isn't falsy.
			if (dataKey === 'oauthTokenData') {
				copiedData[dataKey] = CREDENTIAL_BLANKING_VALUE;
				continue;
			}

			const prop = properties.find((v) => v.name === dataKey);

			if (!prop) {
				continue;
			}

			if (!prop.typeOptions?.password) {
				continue;
			}

			if (prop.noDataExpression) {
				copiedData[dataKey] = CREDENTIAL_BLANKING_VALUE;
				continue;
			}

			if (typeof copiedData[dataKey] === 'string' && !copiedData[dataKey].startsWith('=')) {
				copiedData[dataKey] = CREDENTIAL_BLANKING_VALUE;
				continue;
			}
		}

		return copiedData;
	}

	private unredactRestoreValues(unmerged: any, replacement: any) {
		// eslint-disable-next-line @typescript-eslint/no-unsafe-argument
		for (const [key, value] of Object.entries(unmerged)) {
			if (value === CREDENTIAL_BLANKING_VALUE) {
				// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
				unmerged[key] = replacement[key];
			} else if (
				typeof value === 'object' &&
				value !== null &&
				key in replacement &&
				// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
				typeof replacement[key] === 'object' &&
				// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
				replacement[key] !== null
			) {
				// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
				this.unredactRestoreValues(value, replacement[key]);
			}
		}
	}

	// Take unredacted data (probably from the DB) and merge it with
	// redacted data to create an unredacted version.
	unredact(redactedData: IDataObject, savedData: IDataObject): IDataObject {
		// Replace any blank sentinel values with their saved version
		const mergedData = deepCopy(redactedData ?? {});
		this.unredactRestoreValues(mergedData, savedData);
		return mergedData;
	}

	async saveProviderSettings(providerName: string, data: IDataObject, userId: string) {
		const providerAndSettings = this.externalSecretsManager.getProviderWithSettings(providerName);
		const { settings } = providerAndSettings;
		const newData = this.unredact(data, settings.settings);
		await this.externalSecretsManager.setProviderSettings(providerName, newData, userId);
	}

	async saveProviderConnected(providerName: string, connected: boolean) {
		await this.externalSecretsManager.setProviderConnected(providerName, connected);
		return this.getProvider(providerName);
	}

	getAllSecrets(): Record<string, string[]> {
		return this.externalSecretsManager.getAllSecretNames();
	}

	async testProviderSettings(providerName: string, data: IDataObject) {
		const providerAndSettings = this.externalSecretsManager.getProviderWithSettings(providerName);
		const { settings } = providerAndSettings;
		const newData = this.unredact(data, settings.settings);
		return await this.externalSecretsManager.testProviderSettings(providerName, newData);
	}

	async updateProvider(providerName: string) {
		return await this.externalSecretsManager.updateProvider(providerName);
	}
}
