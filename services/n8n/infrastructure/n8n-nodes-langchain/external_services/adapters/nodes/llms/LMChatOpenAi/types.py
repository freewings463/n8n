"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/llms/LMChatOpenAi/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/llms/LMChatOpenAi 的类型。导入/依赖:外部:@langchain/openai；内部:无；本地:无。导出:BuiltInTools、ModelOptions、PromptOptions、TextOptions、ChatResponseRequest。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/llms/LMChatOpenAi/types.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/llms/LMChatOpenAi/types.py

import type { OpenAIClient } from '@langchain/openai';

export type BuiltInTools = {
	webSearch?: {
		searchContextSize?: 'low' | 'medium' | 'high';
		allowedDomains?: string;
		country?: string;
		city?: string;
		region?: string;
	};
	fileSearch?: {
		vectorStoreIds?: string;
		filters?: string;
		maxResults?: number;
	};
	codeInterpreter?: boolean;
};

export type ModelOptions = {
	baseURL?: string;
	frequencyPenalty?: number;
	maxTokens?: number;
	responseFormat?: 'text' | 'json_object';
	presencePenalty?: number;
	temperature?: number;
	reasoningEffort?: 'low' | 'medium' | 'high';
	timeout?: number;
	maxRetries?: number;
	topP?: number;
	conversationId?: string;
	metadata?: string;
	promptCacheKey?: string;
	safetyIdentifier?: string;
	serviceTier?: 'auto' | 'flex' | 'default' | 'priority';
	topLogprobs?: number;
	textFormat?: {
		textOptions?: TextOptions;
	};
	promptConfig?: {
		promptOptions?: PromptOptions;
	};
};

export type PromptOptions = {
	promptId?: string;
	version?: string;
	variables?: string;
};

export type TextOptions = {
	type?: 'text' | 'json_schema' | 'json_object';
	verbosity?: 'low' | 'medium' | 'high';
	name?: string;
	schema?: string;
	description?: string;
	strict?: boolean;
};
export type ChatResponseRequest = OpenAIClient.Responses.ResponseCreateParamsNonStreaming & {
	conversation?: { id: string } | string;
	top_logprobs?: number;
};
