"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/llms/LmChatAzureOpenAi/credentials/oauth2.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/llms/LmChatAzureOpenAi 的OAuth节点。导入/依赖:外部:@azure/identity；内部:n8n-workflow；本地:./N8nOAuth2TokenCredential。导出:无。关键函数/方法:setupOAuth2Authentication。用于实现 n8n OAuth节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/llms/LmChatAzureOpenAi/credentials/oauth2.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/llms/LmChatAzureOpenAi/credentials/oauth2.py

import { getBearerTokenProvider } from '@azure/identity';
import { NodeOperationError, type ISupplyDataFunctions } from 'n8n-workflow';

import { N8nOAuth2TokenCredential } from './N8nOAuth2TokenCredential';
import type {
	AzureEntraCognitiveServicesOAuth2ApiCredential,
	AzureOpenAIOAuth2ModelConfig,
} from '../types';

const AZURE_OPENAI_SCOPE = 'https://cognitiveservices.azure.com/.default';
/**
 * Creates Entra ID (OAuth2) authentication for Azure OpenAI
 */
export async function setupOAuth2Authentication(
	this: ISupplyDataFunctions,
	credentialName: string,
): Promise<AzureOpenAIOAuth2ModelConfig> {
	try {
		const credential =
			await this.getCredentials<AzureEntraCognitiveServicesOAuth2ApiCredential>(credentialName);
		// Create a TokenCredential
		const entraTokenCredential = new N8nOAuth2TokenCredential(this.getNode(), credential);
		const deploymentDetails = await entraTokenCredential.getDeploymentDetails();

		// Use getBearerTokenProvider to create the function LangChain expects
		// Pass the required scope for Azure Cognitive Services
		const azureADTokenProvider = getBearerTokenProvider(entraTokenCredential, AZURE_OPENAI_SCOPE);

		this.logger.debug('Successfully created Azure AD Token Provider.');

		return {
			azureADTokenProvider,
			azureOpenAIApiInstanceName: deploymentDetails.resourceName,
			azureOpenAIApiVersion: deploymentDetails.apiVersion,
			azureOpenAIEndpoint: deploymentDetails.endpoint,
		};
	} catch (error) {
		this.logger.error(`Error setting up Entra ID authentication: ${error.message}`, error);

		throw new NodeOperationError(
			this.getNode(),
			`Error setting up Entra ID authentication: ${error.message}`,
			error,
		);
	}
}
