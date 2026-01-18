"""
MIGRATION-META:
  source_path: packages/cli/src/modules/external-secrets.ee/providers/gcp-secrets-manager/gcp-secrets-manager.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/external-secrets.ee/providers 的模块。导入/依赖:外部:@google-cloud/secret-manager；内部:@n8n/backend-common、@n8n/di、n8n-workflow；本地:../../constants、../../types。导出:GcpSecretsManager。关键函数/方法:init、update、doConnect、disconnect、getSecret、hasSecret、getSecretNames、parseSecretAccountKey。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/external-secrets.ee/providers/gcp-secrets-manager/gcp-secrets-manager.ts -> services/n8n/tests/cli/unit/modules/external-secrets.ee/providers/gcp-secrets-manager/gcp_secrets_manager.py

import type { protos, SecretManagerServiceClient as GcpClient } from '@google-cloud/secret-manager';
import { Logger } from '@n8n/backend-common';
import { Container } from '@n8n/di';
import { ensureError, jsonParse, type INodeProperties } from 'n8n-workflow';

import type {
	GcpSecretsManagerContext,
	GcpSecretAccountKey,
	RawGcpSecretAccountKey,
} from './types';
import { DOCS_HELP_NOTICE, EXTERNAL_SECRETS_NAME_REGEX } from '../../constants';
import { SecretsProvider } from '../../types';

export class GcpSecretsManager extends SecretsProvider {
	name = 'gcpSecretsManager';

	displayName = 'GCP Secrets Manager';

	properties: INodeProperties[] = [
		DOCS_HELP_NOTICE,
		{
			displayName: 'Service Account Key',
			name: 'serviceAccountKey',
			type: 'string',
			default: '',
			required: true,
			typeOptions: { password: true },
			placeholder: 'e.g. { "type": "service_account", "project_id": "gcp-secrets-store", ... }',
			hint: 'Content of JSON file downloaded from Google Cloud Console.',
			noDataExpression: true,
		},
	];

	private cachedSecrets: Record<string, string> = {};

	private client: GcpClient;

	private settings: GcpSecretAccountKey;

	constructor(private readonly logger = Container.get(Logger)) {
		super();
		this.logger = this.logger.scoped('external-secrets');
	}

	async init(context: GcpSecretsManagerContext) {
		this.settings = this.parseSecretAccountKey(context.settings.serviceAccountKey);
	}

	protected async doConnect(): Promise<void> {
		const { projectId, privateKey, clientEmail } = this.settings;

		const { SecretManagerServiceClient: GcpClient } = await import('@google-cloud/secret-manager');

		this.client = new GcpClient({
			credentials: { client_email: clientEmail, private_key: privateKey },
			projectId,
		});

		this.logger.debug('GCP Secrets Manager provider connected');
	}

	async test(): Promise<[boolean] | [boolean, string]> {
		if (!this.client) return [false, 'Failed to connect to GCP Secrets Manager'];

		try {
			await this.client.initialize();
			return [true];
		} catch (error: unknown) {
			return [false, error instanceof Error ? error.message : 'Unknown error'];
		}
	}

	async disconnect() {
		// unused
	}

	async update() {
		const { projectId } = this.settings;

		const [rawSecretNames] = await this.client.listSecrets({
			parent: `projects/${projectId}`,
		});

		const secretNames = rawSecretNames.reduce<string[]>((acc, cur) => {
			if (!cur.name || !EXTERNAL_SECRETS_NAME_REGEX.test(cur.name)) return acc;

			const secretName = cur.name.split('/').pop();

			if (secretName) acc.push(secretName);

			return acc;
		}, []);

		const promises = secretNames.map(async (name) => {
			let versions:
				| [
						protos.google.cloud.secretmanager.v1.IAccessSecretVersionResponse,
						protos.google.cloud.secretmanager.v1.IAccessSecretVersionRequest | undefined,
						{} | undefined,
				  ]
				| undefined;

			try {
				versions = await this.client.accessSecretVersion({
					name: `projects/${projectId}/secrets/${name}/versions/latest`,
				});
			} catch (error) {
				// Only handle expected error codes that indicate the secret is not accessible
				// PERMISSION_DENIED (7), NOT_FOUND (5), UNAVAILABLE (14)
				const errorCode = error?.code;
				if (errorCode === 7 || errorCode === 5 || errorCode === 14) {
					this.logger.info(
						`Skipping GCP secret: ${name}, version: latest as the version is not accessible`,
						{
							error: ensureError(error),
						},
					);
				} else {
					// Rethrow unexpected errors to avoid masking broader failures
					throw error;
				}
			}

			if (!Array.isArray(versions) || !versions.length) return null;

			const [latestVersion] = versions;

			if (!latestVersion.payload?.data) return null;

			const value = latestVersion.payload.data.toString();

			if (!value) return null;

			return { name, value };
		});

		const results = await Promise.all(promises);

		this.cachedSecrets = results.reduce<Record<string, string>>((acc, cur) => {
			if (cur) acc[cur.name] = cur.value;
			return acc;
		}, {});

		this.logger.debug('GCP Secrets Manager provider secrets updated');
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

	private parseSecretAccountKey(privateKey: string): GcpSecretAccountKey {
		const parsed = jsonParse<RawGcpSecretAccountKey>(privateKey, { fallbackValue: {} });

		return {
			projectId: parsed?.project_id ?? '',
			clientEmail: parsed?.client_email ?? '',
			privateKey: parsed?.private_key ?? '',
		};
	}
}
