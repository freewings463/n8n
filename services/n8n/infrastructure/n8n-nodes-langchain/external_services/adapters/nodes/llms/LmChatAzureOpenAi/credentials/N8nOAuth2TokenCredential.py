"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/llms/LmChatAzureOpenAi/credentials/N8nOAuth2TokenCredential.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/llms/LmChatAzureOpenAi 的OAuth节点。导入/依赖:外部:@azure/identity；内部:@n8n/client-oauth2、n8n-workflow；本地:../types。导出:N8nOAuth2TokenCredential。关键函数/方法:getToken、getDeploymentDetails。用于实现 n8n OAuth节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/llms/LmChatAzureOpenAi/credentials/N8nOAuth2TokenCredential.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/llms/LmChatAzureOpenAi/credentials/N8nOAuth2TokenCredential.py

import type { TokenCredential, AccessToken } from '@azure/identity';
import type { ClientOAuth2TokenData } from '@n8n/client-oauth2';
import { ClientOAuth2 } from '@n8n/client-oauth2';
import type { INode } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import type { AzureEntraCognitiveServicesOAuth2ApiCredential } from '../types';
/**
 * Adapts n8n's credential retrieval into the TokenCredential interface expected by @azure/identity
 */
export class N8nOAuth2TokenCredential implements TokenCredential {
	constructor(
		private node: INode,
		private credential: AzureEntraCognitiveServicesOAuth2ApiCredential,
	) {}

	/**
	 * Gets an access token from OAuth credential
	 */
	async getToken(): Promise<AccessToken | null> {
		try {
			if (!this.credential?.oauthTokenData?.access_token) {
				throw new NodeOperationError(this.node, 'Failed to retrieve access token');
			}
			const oAuthClient = new ClientOAuth2({
				clientId: this.credential.clientId,
				clientSecret: this.credential.clientSecret,
				accessTokenUri: this.credential.accessTokenUrl,
				scopes: this.credential.scope?.split(' '),
				authentication: this.credential.authentication,
				authorizationUri: this.credential.authUrl,
				additionalBodyProperties: {
					resource: 'https://cognitiveservices.azure.com/',
				},
			});

			const token = await oAuthClient.credentials.getToken();
			const data = token.data as ClientOAuth2TokenData & {
				expires_on: number;
			};
			return {
				token: data.access_token,
				expiresOnTimestamp: data.expires_on,
			};
		} catch (error) {
			// Re-throw with better error message
			throw new NodeOperationError(this.node, 'Failed to retrieve OAuth2 access token', error);
		}
	}

	/**
	 * Gets the deployment details from the credential
	 */
	async getDeploymentDetails() {
		return {
			apiVersion: this.credential.apiVersion,
			endpoint: this.credential.endpoint,
			resourceName: this.credential.resourceName,
		};
	}
}
