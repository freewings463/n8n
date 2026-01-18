"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/llms/LmChatAzureOpenAi/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/llms/LmChatAzureOpenAi 的类型。导入/依赖:外部:无；内部:@n8n/client-oauth2；本地:无。导出:AzureOpenAIConfig、AzureOpenAIApiKeyConfig、AzureOpenAIOptions、AzureOpenAIBaseModelConfig、AzureOpenAIApiKeyModelConfig、AzureOpenAIOAuth2ModelConfig、enum、AzureEntraCognitiveServicesOAuth2ApiCredential。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/llms/LmChatAzureOpenAi/types.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/llms/LmChatAzureOpenAi/types.py

import type { OAuth2CredentialData } from '@n8n/client-oauth2';
/**
 * Common interfaces for Azure OpenAI configuration
 */

/**
 * Basic Azure OpenAI API configuration options
 */
export interface AzureOpenAIConfig {
	apiVersion: string;
	resourceName: string;
	endpoint?: string;
}

/**
 * Configuration for API Key authentication
 */
export interface AzureOpenAIApiKeyConfig extends AzureOpenAIConfig {
	apiKey: string;
}

/**
 * Azure OpenAI node options
 */
export interface AzureOpenAIOptions {
	frequencyPenalty?: number;
	maxTokens?: number;
	maxRetries?: number;
	timeout?: number;
	presencePenalty?: number;
	temperature?: number;
	topP?: number;
	responseFormat?: 'text' | 'json_object';
}

/**
 * Base model configuration that can be passed to AzureChatOpenAI constructor
 */
export interface AzureOpenAIBaseModelConfig {
	azureOpenAIApiInstanceName: string;
	azureOpenAIApiVersion: string;
	azureOpenAIEndpoint?: string;
}

/**
 * API Key model configuration that can be passed to AzureChatOpenAI constructor
 */
export interface AzureOpenAIApiKeyModelConfig extends AzureOpenAIBaseModelConfig {
	azureOpenAIApiKey: string;
	azureADTokenProvider?: undefined;
}

/**
 * OAuth2 model configuration that can be passed to AzureChatOpenAI constructor
 */
export interface AzureOpenAIOAuth2ModelConfig extends AzureOpenAIBaseModelConfig {
	azureOpenAIApiKey?: undefined;
	azureADTokenProvider: () => Promise<string>;
}

/**
 * Authentication types supported by Azure OpenAI node
 */
export const enum AuthenticationType {
	ApiKey = 'azureOpenAiApi',
	EntraOAuth2 = 'azureEntraCognitiveServicesOAuth2Api',
}

/**
 * Error types for Azure OpenAI node
 */
export const enum AzureOpenAIErrorType {
	AuthenticationError = 'AuthenticationError',
	ConfigurationError = 'ConfigurationError',
	APIError = 'APIError',
	UnknownError = 'UnknownError',
}

/**
 * OAuth2 credential type used by Azure OpenAI node
 */
type TokenData = OAuth2CredentialData['oauthTokenData'] & {
	expires_on: number;
	ext_expires_on: number;
};
export type AzureEntraCognitiveServicesOAuth2ApiCredential = OAuth2CredentialData & {
	customScopes: boolean;
	authentication: string;
	apiVersion: string;
	endpoint: string;
	resourceName: string;
	tenantId: string;
	oauthTokenData: TokenData;
};
