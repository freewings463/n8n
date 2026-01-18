"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/llms/LmChatAzureOpenAi/credentials/api-key.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/llms/LmChatAzureOpenAi 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../types。导出:无。关键函数/方法:setupApiKeyAuthentication。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/llms/LmChatAzureOpenAi/credentials/api-key.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/llms/LmChatAzureOpenAi/credentials/api_key.py

import { NodeOperationError, OperationalError, type ISupplyDataFunctions } from 'n8n-workflow';

import type { AzureOpenAIApiKeyModelConfig } from '../types';

/**
 * Handles API Key authentication setup for Azure OpenAI
 */
export async function setupApiKeyAuthentication(
	this: ISupplyDataFunctions,
	credentialName: string,
): Promise<AzureOpenAIApiKeyModelConfig> {
	try {
		// Get Azure OpenAI Config (Endpoint, Version, etc.)
		const configCredentials = await this.getCredentials<{
			apiKey?: string;
			resourceName: string;
			apiVersion: string;
			endpoint?: string;
		}>(credentialName);

		if (!configCredentials.apiKey) {
			throw new NodeOperationError(
				this.getNode(),
				'API Key is missing in the selected Azure OpenAI API credential. Please configure the API Key or choose Entra ID authentication.',
			);
		}

		this.logger.info('Using API Key authentication for Azure OpenAI.');

		return {
			azureOpenAIApiKey: configCredentials.apiKey,
			azureOpenAIApiInstanceName: configCredentials.resourceName,
			azureOpenAIApiVersion: configCredentials.apiVersion,
			azureOpenAIEndpoint: configCredentials.endpoint,
		};
	} catch (error) {
		if (error instanceof OperationalError) {
			throw error;
		}

		this.logger.error(`Error setting up API Key authentication: ${error.message}`, error);

		throw new NodeOperationError(this.getNode(), 'Failed to retrieve API Key', error);
	}
}
