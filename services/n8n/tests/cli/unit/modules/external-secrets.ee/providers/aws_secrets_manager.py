"""
MIGRATION-META:
  source_path: packages/cli/src/modules/external-secrets.ee/providers/aws-secrets-manager.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/external-secrets.ee/providers 的模块。导入/依赖:外部:@aws-sdk/client-secrets-manager；内部:@n8n/backend-common、@n8n/di 等1项；本地:../constants、../errors/unknown-auth-type.error、../types。导出:AwsSecretsManagerContext、AwsSecretsManager。关键函数/方法:init、update、doConnect、disconnect、getSecret、hasSecret、getSecretNames、assertAuthType、fetchAllSecretsNames、fetchAllSecrets。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/external-secrets.ee/providers/aws-secrets-manager.ts -> services/n8n/tests/cli/unit/modules/external-secrets.ee/providers/aws_secrets_manager.py

import { SecretsManager, type SecretsManagerClientConfig } from '@aws-sdk/client-secrets-manager';
import { Logger } from '@n8n/backend-common';
import { Container } from '@n8n/di';
import type { INodeProperties } from 'n8n-workflow';

import { DOCS_HELP_NOTICE, EXTERNAL_SECRETS_NAME_REGEX } from '../constants';
import { UnknownAuthTypeError } from '../errors/unknown-auth-type.error';
import { SecretsProvider } from '../types';
import type { SecretsProviderSettings } from '../types';

type Secret = {
	secretName: string;
	secretValue: string;
};

export type AwsSecretsManagerContext = SecretsProviderSettings<
	{
		region: string;
	} & (
		| {
				authMethod: 'iamUser';
				accessKeyId: string;
				secretAccessKey: string;
		  }
		| { authMethod: 'autoDetect' }
	)
>;

export class AwsSecretsManager extends SecretsProvider {
	name = 'awsSecretsManager';

	displayName = 'AWS Secrets Manager';

	properties: INodeProperties[] = [
		DOCS_HELP_NOTICE,
		{
			displayName: 'Region',
			name: 'region',
			type: 'string',
			default: '',
			required: true,
			placeholder: 'e.g. eu-west-3',
			noDataExpression: true,
		},
		{
			displayName: 'Authentication Method',
			name: 'authMethod',
			type: 'options',
			options: [
				{
					name: 'IAM User',
					value: 'iamUser',
					description:
						'Credentials for IAM user having <code>secretsmanager:ListSecrets</code> and <code>secretsmanager:BatchGetSecretValue</code> permissions. <a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html" target="_blank">Learn more</a>',
				},
				{
					name: 'Auto Detect',
					value: 'autoDetect',
					description:
						'Use automatic credential detection to authenticate AWS calls for external secrets<a href="https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/setting-credentials-node.html#credchain" target="_blank">Learn more</a>.',
				},
			],
			default: 'iamUser',
			required: true,
			noDataExpression: true,
		},
		{
			displayName: 'Access Key ID',
			name: 'accessKeyId',
			type: 'string',
			default: '',
			required: true,
			placeholder: 'e.g. ACHXUQMBAQEVTE2RKMWP',
			noDataExpression: true,
			displayOptions: {
				show: {
					authMethod: ['iamUser'],
				},
			},
		},
		{
			displayName: 'Secret Access Key',
			name: 'secretAccessKey',
			type: 'string',
			default: '',
			required: true,
			placeholder: 'e.g. cbmjrH/xNAjPwlQR3i/1HRSDD+esQX/Lan3gcmBc',
			typeOptions: { password: true },
			noDataExpression: true,
			displayOptions: {
				show: {
					authMethod: ['iamUser'],
				},
			},
		},
	];

	private cachedSecrets: Record<string, string> = {};

	private client: SecretsManager;

	constructor(private readonly logger = Container.get(Logger)) {
		super();
		this.logger = this.logger.scoped('external-secrets');
	}

	async init(context: AwsSecretsManagerContext) {
		this.assertAuthType(context);

		const { region, authMethod } = context.settings;
		const clientConfig: SecretsManagerClientConfig = { region };

		if (authMethod === 'iamUser') {
			const { accessKeyId, secretAccessKey } = context.settings;
			clientConfig.credentials = { accessKeyId, secretAccessKey };
		}

		this.client = new SecretsManager(clientConfig);

		this.logger.debug('AWS Secrets Manager provider initialized');
	}

	async test(): Promise<[boolean] | [boolean, string]> {
		try {
			await this.client.listSecrets({ MaxResults: 1 });
			return [true];
		} catch (e) {
			const error = e instanceof Error ? e : new Error(`${e}`);
			return [false, error.message];
		}
	}

	protected async doConnect(): Promise<void> {
		const [wasSuccessful, errorMsg] = await this.test();

		if (!wasSuccessful) {
			throw new Error(errorMsg || 'Connection failed');
		}

		this.logger.debug('AWS Secrets Manager provider connected');
	}

	async disconnect() {
		return;
	}

	async update() {
		const secrets = await this.fetchAllSecrets();

		const supportedSecrets = secrets.filter((s) => EXTERNAL_SECRETS_NAME_REGEX.test(s.secretName));

		this.cachedSecrets = Object.fromEntries(
			supportedSecrets.map((s) => [s.secretName, s.secretValue]),
		);

		this.logger.debug('AWS Secrets Manager provider secrets updated');
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

	private assertAuthType(context: AwsSecretsManagerContext) {
		const { authMethod } = context.settings;
		if (authMethod === 'iamUser' || authMethod === 'autoDetect') return;
		throw new UnknownAuthTypeError(authMethod);
	}

	private async fetchAllSecretsNames() {
		const names: string[] = [];
		let nextToken: string | undefined;

		do {
			const response = await this.client.listSecrets({
				NextToken: nextToken,
			});

			if (response.SecretList) {
				names.push(...response.SecretList.filter((s) => s.Name).map((s) => s.Name!));
			}

			nextToken = response.NextToken;
		} while (nextToken);

		return names;
	}

	private async fetchAllSecrets() {
		const secrets: Secret[] = [];
		const secretNames = await this.fetchAllSecretsNames();

		// Batch the requests to avoid hitting limits
		const batches = this.batch(secretNames);

		for (const batch of batches) {
			const response = await this.client.batchGetSecretValue({
				SecretIdList: batch,
			});

			if (response.SecretValues) {
				for (const secret of response.SecretValues) {
					if (secret.Name && secret.SecretString) {
						secrets.push({
							secretName: secret.Name,
							secretValue: secret.SecretString,
						});
					}
				}
			}
		}

		return secrets;
	}

	private batch<T>(arr: T[], size = 20): T[][] {
		return Array.from({ length: Math.ceil(arr.length / size) }, (_, index) =>
			arr.slice(index * size, (index + 1) * size),
		);
	}
}
