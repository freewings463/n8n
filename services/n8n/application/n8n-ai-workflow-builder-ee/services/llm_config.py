"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/llm-config.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src 的工作流配置。导入/依赖:外部:@langchain/openai、@langchain/anthropic；内部:@/constants；本地:./utils/http-proxy-agent。导出:o4mini、gpt41mini、gpt41、anthropicClaudeSonnet45、anthropicHaiku45。关键函数/方法:o4mini、gpt41mini、gpt41、anthropicClaudeSonnet45、anthropicHaiku45。用于集中定义工作流配置项与默认值，供其他模块读取。注释目标:Different LLMConfig type for this file - specific to LLM providers。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/llm-config.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/llm_config.py

// Different LLMConfig type for this file - specific to LLM providers
import { MAX_OUTPUT_TOKENS } from '@/constants';

import { getProxyAgent } from './utils/http-proxy-agent';

interface LLMProviderConfig {
	apiKey: string;
	baseUrl?: string;
	headers?: Record<string, string>;
}

export const o4mini = async (config: LLMProviderConfig) => {
	const { ChatOpenAI } = await import('@langchain/openai');
	return new ChatOpenAI({
		model: 'o4-mini-2025-04-16',
		apiKey: config.apiKey,
		configuration: {
			baseURL: config.baseUrl,
			defaultHeaders: config.headers,
			fetchOptions: {
				dispatcher: getProxyAgent(config.baseUrl ?? 'https://api.openai.com/v1'),
			},
		},
	});
};

export const gpt41mini = async (config: LLMProviderConfig) => {
	const { ChatOpenAI } = await import('@langchain/openai');
	return new ChatOpenAI({
		model: 'gpt-4.1-mini-2025-04-14',
		apiKey: config.apiKey,
		temperature: 0,
		maxTokens: -1,
		configuration: {
			baseURL: config.baseUrl,
			defaultHeaders: config.headers,
			fetchOptions: {
				dispatcher: getProxyAgent(config.baseUrl ?? 'https://api.openai.com/v1'),
			},
		},
	});
};

export const gpt41 = async (config: LLMProviderConfig) => {
	const { ChatOpenAI } = await import('@langchain/openai');
	return new ChatOpenAI({
		model: 'gpt-4.1-2025-04-14',
		apiKey: config.apiKey,
		temperature: 0.3,
		maxTokens: -1,
		configuration: {
			baseURL: config.baseUrl,
			defaultHeaders: config.headers,
			fetchOptions: {
				dispatcher: getProxyAgent(config.baseUrl ?? 'https://api.openai.com/v1'),
			},
		},
	});
};

export const anthropicClaudeSonnet45 = async (config: LLMProviderConfig) => {
	const { ChatAnthropic } = await import('@langchain/anthropic');
	const model = new ChatAnthropic({
		model: 'claude-sonnet-4-5',
		apiKey: config.apiKey,
		temperature: 0,
		maxTokens: MAX_OUTPUT_TOKENS,
		anthropicApiUrl: config.baseUrl,
		clientOptions: {
			defaultHeaders: config.headers,
			fetchOptions: {
				dispatcher: getProxyAgent(config.baseUrl),
			},
		},
	});

	// Remove Langchain default topP parameter since Sonnet 4.5 doesn't allow setting both temperature and topP
	delete model.topP;

	return model;
};

export const anthropicHaiku45 = async (config: LLMProviderConfig) => {
	const { ChatAnthropic } = await import('@langchain/anthropic');
	const model = new ChatAnthropic({
		model: 'claude-haiku-4-5-20251001',
		apiKey: config.apiKey,
		temperature: 0,
		maxTokens: MAX_OUTPUT_TOKENS,
		anthropicApiUrl: config.baseUrl,
		clientOptions: {
			defaultHeaders: config.headers,
			fetchOptions: {
				dispatcher: getProxyAgent(config.baseUrl),
			},
		},
	});

	// Remove Langchain default topP parameter since Sonnet 4.5 doesn't allow setting both temperature and topP
	delete model.topP;

	return model;
};
