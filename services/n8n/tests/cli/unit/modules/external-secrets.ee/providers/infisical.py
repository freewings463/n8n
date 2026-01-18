"""
MIGRATION-META:
  source_path: packages/cli/src/modules/external-secrets.ee/providers/infisical.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/external-secrets.ee/providers 的模块。导入/依赖:外部:infisical-node、infisical-node/…/serviceTokenData、infisical-node/…/key；内部:n8n-workflow；本地:../constants、../types。导出:InfisicalSettings、InfisicalProvider。关键函数/方法:init、update、secrets、doConnect、getEnvironment、serviceTokenData、disconnect、getSecret、getSecretNames、hasSecret。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/external-secrets.ee/providers/infisical.ts -> services/n8n/tests/cli/unit/modules/external-secrets.ee/providers/infisical.py

import InfisicalClient from 'infisical-node';
import { getServiceTokenData } from 'infisical-node/lib/api/serviceTokenData';
import { populateClientWorkspaceConfigsHelper } from 'infisical-node/lib/helpers/key';
import { UnexpectedError, type IDataObject, type INodeProperties } from 'n8n-workflow';

import { EXTERNAL_SECRETS_NAME_REGEX } from '../constants';
import { SecretsProvider } from '../types';
import type { SecretsProviderSettings } from '../types';

export interface InfisicalSettings {
	token: string;
	siteURL: string;
	cacheTTL: number;
	debug: boolean;
}

interface InfisicalSecret {
	secretName: string;
	secretValue?: string;
}

interface InfisicalServiceToken {
	environment?: string;
	scopes?: Array<{ environment: string; path: string }>;
}

export class InfisicalProvider extends SecretsProvider {
	properties: INodeProperties[] = [
		{
			displayName:
				'<h2>Important information about our infisical integration</h2><br>From the <b>30th July, 2024</b>, we will no longer be supporting new connections to inifiscal secrets vault using service tokens. Existing service tokens will remain usable until <b>July, 2025</b>. After that period, we will be removing support for Infisical from our external secrets integrations. You can find out more information about this change on <a href="https://docs.n8n.io/external-secrets/#connect-n8n-to-your-secrets-store" target="_blank">our docs</a>',
			name: 'notice',
			type: 'notice',
			default: '',
			noDataExpression: true,
		},
		{
			displayName: 'Service Token',
			name: 'token',
			type: 'string',
			hint: 'The Infisical Service Token with read access',
			default: '',
			required: true,
			placeholder: 'e.g. st.64ae963e1874ea.374226a166439dce.39557e4a1b7bdd82',
			noDataExpression: true,
			typeOptions: { password: true },
		},
		{
			displayName: 'Site URL',
			name: 'siteURL',
			type: 'string',
			hint: "The absolute URL of the Infisical instance. Change it only if you're self-hosting Infisical.",
			required: true,
			noDataExpression: true,
			placeholder: 'https://app.infisical.com',
			default: 'https://app.infisical.com',
		},
	];

	displayName = 'Infisical';

	name = 'infisical';

	private cachedSecrets: Record<string, string> = {};

	private client: InfisicalClient;

	private settings: InfisicalSettings;

	private environment: string;

	async init(settings: SecretsProviderSettings): Promise<void> {
		this.settings = settings.settings as unknown as InfisicalSettings;
	}

	async update(): Promise<void> {
		if (!this.client) {
			throw new UnexpectedError('Updated attempted on Infisical when initialization failed');
		}
		if (!(await this.test())[0]) {
			throw new UnexpectedError('Infisical provider test failed during update');
		}
		const secrets = (await this.client.getAllSecrets({
			environment: this.environment,
			path: '/',
			attachToProcessEnv: false,
			includeImports: true,
		})) as InfisicalSecret[];
		const newCache = Object.fromEntries(
			secrets.map((s) => [s.secretName, s.secretValue]),
		) as Record<string, string>;
		if (Object.keys(newCache).length === 1 && '' in newCache) {
			this.cachedSecrets = {};
		} else {
			this.cachedSecrets = newCache;
		}
	}

	protected async doConnect(): Promise<void> {
		this.client = new InfisicalClient(this.settings);

		const [testSuccess] = await this.test();
		if (!testSuccess) {
			throw new Error('Connection test failed');
		}

		this.environment = await this.getEnvironment();
	}

	async getEnvironment(): Promise<string> {
		const serviceTokenData = (await getServiceTokenData(
			// eslint-disable-next-line @typescript-eslint/no-unsafe-argument
			this.client.clientConfig,
		)) as InfisicalServiceToken;
		if (serviceTokenData.environment) {
			return serviceTokenData.environment;
		}
		if (serviceTokenData.scopes) {
			return serviceTokenData.scopes[0].environment;
		}
		throw new UnexpectedError("Couldn't find environment for Infisical");
	}

	async test(): Promise<[boolean] | [boolean, string]> {
		if (!this.client) {
			return [false, 'Client not initialized'];
		}
		try {
			await populateClientWorkspaceConfigsHelper(this.client.clientConfig);
			return [true];
		} catch (e) {
			return [false];
		}
	}

	async disconnect(): Promise<void> {
		//
	}

	getSecret(name: string): IDataObject {
		return this.cachedSecrets[name] as unknown as IDataObject;
	}

	getSecretNames(): string[] {
		return Object.keys(this.cachedSecrets).filter((k) => EXTERNAL_SECRETS_NAME_REGEX.test(k));
	}

	hasSecret(name: string): boolean {
		return name in this.cachedSecrets;
	}
}
