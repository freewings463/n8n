"""
MIGRATION-META:
  source_path: packages/cli/src/modules/external-secrets.ee/providers/azure-key-vault/azure-key-vault.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/external-secrets.ee/providers 的模块。导入/依赖:外部:@azure/keyvault-secrets、@azure/identity；内部:@n8n/backend-common、@n8n/di、n8n-workflow；本地:./types、../../constants、../../types。导出:AzureKeyVault。关键函数/方法:init、update、doConnect、disconnect、getSecret、hasSecret、getSecretNames。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/external-secrets.ee/providers/azure-key-vault/azure-key-vault.ts -> services/n8n/tests/cli/unit/modules/external-secrets.ee/providers/azure-key-vault/azure_key_vault.py

import type { SecretClient } from '@azure/keyvault-secrets';
import { Logger } from '@n8n/backend-common';
import { Container } from '@n8n/di';
import type { INodeProperties } from 'n8n-workflow';

import type { AzureKeyVaultContext } from './types';
import { DOCS_HELP_NOTICE, EXTERNAL_SECRETS_NAME_REGEX } from '../../constants';
import { SecretsProvider } from '../../types';

export class AzureKeyVault extends SecretsProvider {
	name = 'azureKeyVault';

	displayName = 'Azure Key Vault';

	properties: INodeProperties[] = [
		DOCS_HELP_NOTICE,
		{
			displayName: 'Vault Name',
			hint: 'The name of your existing Azure Key Vault.',
			name: 'vaultName',
			type: 'string',
			default: '',
			required: true,
			placeholder: 'e.g. my-vault',
			noDataExpression: true,
		},
		{
			displayName: 'Tenant ID',
			name: 'tenantId',
			hint: 'In Azure, this can be called "Directory (Tenant) ID".',
			type: 'string',
			default: '',
			required: true,
			placeholder: 'e.g. 7dec9324-7074-72b7-a3ca-a9bb3012f466',
			noDataExpression: true,
		},
		{
			displayName: 'Client ID',
			name: 'clientId',
			hint: 'In Azure, this can be called "Application (Client) ID".',
			type: 'string',
			default: '',
			required: true,
			placeholder: 'e.g. 7753d8c2-e41f-22ed-3dd7-c9e96463622c',
			typeOptions: { password: true },
			noDataExpression: true,
		},
		{
			displayName: 'Client Secret',
			name: 'clientSecret',
			hint: 'The client secret value of your registered application.',
			type: 'string',
			default: '',
			required: true,
			typeOptions: { password: true },
			noDataExpression: true,
		},
	];

	private cachedSecrets: Record<string, string> = {};

	private client: SecretClient;

	private settings: AzureKeyVaultContext['settings'];

	constructor(private readonly logger = Container.get(Logger)) {
		super();
		this.logger = this.logger.scoped('external-secrets');
	}

	async init(context: AzureKeyVaultContext) {
		this.settings = context.settings;

		this.logger.debug('Azure Key Vault provider initialized');
	}

	protected async doConnect(): Promise<void> {
		const { vaultName, tenantId, clientId, clientSecret } = this.settings;

		const { ClientSecretCredential } = await import('@azure/identity');
		const { SecretClient } = await import('@azure/keyvault-secrets');

		const credential = new ClientSecretCredential(tenantId, clientId, clientSecret);
		this.client = new SecretClient(`https://${vaultName}.vault.azure.net/`, credential);

		this.logger.debug('Azure Key Vault provider connected');
	}

	async test(): Promise<[boolean] | [boolean, string]> {
		if (!this.client) return [false, 'Failed to connect to Azure Key Vault'];

		try {
			await this.client.listPropertiesOfSecrets().next();
			return [true];
		} catch (error: unknown) {
			return [false, error instanceof Error ? error.message : 'Unknown error'];
		}
	}

	async disconnect() {
		// unused
	}

	async update() {
		const secretNames: string[] = [];

		for await (const secret of this.client.listPropertiesOfSecrets()) {
			secretNames.push(secret.name);
		}

		const promises = secretNames
			.filter((name) => EXTERNAL_SECRETS_NAME_REGEX.test(name))
			.map(async (name) => {
				const { value } = await this.client.getSecret(name);
				return { name, value };
			});

		const secrets = await Promise.all(promises);

		this.cachedSecrets = secrets.reduce<Record<string, string>>((acc, cur) => {
			if (cur.value === undefined) return acc;
			acc[cur.name] = cur.value;
			return acc;
		}, {});

		this.logger.debug('Azure Key Vault provider secrets updated');
	}

	getSecret(name: string) {
		return this.cachedSecrets[name];
	}

	hasSecret(name: string) {
		return name in this.cachedSecrets;
	}

	getSecretNames() {
		return Object.keys(this.cachedSecrets);
	}
}
