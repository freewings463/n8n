"""
MIGRATION-META:
  source_path: packages/cli/src/credentials/dynamic-credentials-proxy.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/credentials 的凭证。导入/依赖:外部:无；内部:@n8n/backend-common、@n8n/di、n8n-core、n8n-workflow；本地:无。导出:DynamicCredentialsProxy。关键函数/方法:setStorageProvider、setResolverProvider、resolveIfNeeded、storeIfNeeded、storeOAuthTokenDataIfNeeded。用于声明 n8n 该模块鉴权字段/校验规则，供节点引用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/credentials/dynamic-credentials-proxy.ts -> services/n8n/application/cli/services/credentials/dynamic_credentials_proxy.py

import { Logger } from '@n8n/backend-common';
import { Container, Service } from '@n8n/di';
import { Cipher } from 'n8n-core';
import type {
	ICredentialContext,
	ICredentialDataDecryptedObject,
	IDataObject,
	IExecutionContext,
	IWorkflowSettings,
} from 'n8n-workflow';
import { toCredentialContext, UnexpectedError } from 'n8n-workflow';

import type {
	CredentialResolveMetadata,
	ICredentialResolutionProvider,
} from './credential-resolution-provider.interface';
import type {
	CredentialStoreMetadata,
	IDynamicCredentialStorageProvider,
} from './dynamic-credential-storage.interface';

@Service()
export class DynamicCredentialsProxy
	implements IDynamicCredentialStorageProvider, ICredentialResolutionProvider
{
	private storageProvider: IDynamicCredentialStorageProvider;
	private resolvingProvider: ICredentialResolutionProvider;

	constructor(private readonly logger: Logger) {}

	setStorageProvider(provider: IDynamicCredentialStorageProvider) {
		this.storageProvider = provider;
	}

	setResolverProvider(provider: ICredentialResolutionProvider) {
		this.resolvingProvider = provider;
	}

	async resolveIfNeeded(
		credentialsResolveMetadata: CredentialResolveMetadata,
		staticData: ICredentialDataDecryptedObject,
		executionContext?: IExecutionContext,
		workflowSettings?: IWorkflowSettings,
		canUseExternalSecrets?: boolean,
	): Promise<ICredentialDataDecryptedObject> {
		if (!this.resolvingProvider) {
			if (credentialsResolveMetadata.isResolvable) {
				this.logger.warn(
					`No dynamic credential resolving provider set, but trying to resolve resolvable credential "${credentialsResolveMetadata.name}"`,
				);
				throw new Error('No dynamic credential resolving provider set');
			}
			return staticData;
		}
		return await this.resolvingProvider.resolveIfNeeded(
			credentialsResolveMetadata,
			staticData,
			executionContext,
			workflowSettings,
			canUseExternalSecrets,
		);
	}

	async storeIfNeeded(
		credentialStoreMetadata: CredentialStoreMetadata,
		dynamicData: ICredentialDataDecryptedObject,
		credentialContext: ICredentialContext,
		staticData?: ICredentialDataDecryptedObject,
		workflowSettings?: IWorkflowSettings,
	): Promise<void> {
		if (!this.storageProvider) {
			if (credentialStoreMetadata.isResolvable) {
				this.logger.warn(
					`No dynamic credential storage provider set, but trying to store resolvable credential "${credentialStoreMetadata.name}"`,
				);
				throw new Error('No dynamic credential storage provider set');
			}
			return;
		}
		return await this.storageProvider.storeIfNeeded(
			credentialStoreMetadata,
			dynamicData,
			credentialContext,
			staticData,
			workflowSettings,
		);
	}

	/**
	 * Stores OAuth token data for dynamic credentials, handling execution context decryption
	 */
	async storeOAuthTokenDataIfNeeded(
		credentialStoreMetadata: CredentialStoreMetadata,
		oauthTokenData: IDataObject,
		executionContext: IExecutionContext | undefined,
		staticData: ICredentialDataDecryptedObject,
		workflowSettings?: IWorkflowSettings,
	): Promise<void> {
		if (!credentialStoreMetadata.isResolvable || !credentialStoreMetadata.resolverId) {
			return;
		}

		const cipher = Container.get(Cipher);

		let credentialContext: { version: 1; identity: string } | undefined;

		if (executionContext?.credentials) {
			const decrypted = cipher.decrypt(executionContext.credentials);
			credentialContext = toCredentialContext(decrypted) as { version: 1; identity: string };
		}

		if (!credentialContext) {
			throw new UnexpectedError('No credential context found', {
				extra: {
					credentialId: credentialStoreMetadata.id,
					credentialName: credentialStoreMetadata.name,
				},
			});
		}

		await this.storeIfNeeded(
			credentialStoreMetadata,
			{ oauthTokenData } as ICredentialDataDecryptedObject,
			credentialContext,
			staticData,
			workflowSettings,
		);
	}
}
