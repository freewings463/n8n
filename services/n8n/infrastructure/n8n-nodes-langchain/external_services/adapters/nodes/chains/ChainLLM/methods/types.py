"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/chains/ChainLLM/methods/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/chains/ChainLLM 的类型。导入/依赖:外部:@langchain/core/…/base、@langchain/core/…/chat_models、@utils/output_parsers/N8nOutputParser；内部:n8n-workflow；本地:无。导出:MessageTemplate、PromptParams、ChainExecutionParams。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/chains/ChainLLM/methods/types.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/chains/ChainLLM/methods/types.py

import type { BaseLanguageModel } from '@langchain/core/language_models/base';
import type { BaseChatModel } from '@langchain/core/language_models/chat_models';
import type { IExecuteFunctions } from 'n8n-workflow';

import type { N8nOutputParser } from '@utils/output_parsers/N8nOutputParser';

/**
 * Interface for describing a message template in the UI
 */
export interface MessageTemplate {
	type: string;
	message: string;
	messageType: 'text' | 'imageBinary' | 'imageUrl';
	binaryImageDataKey?: string;
	imageUrl?: string;
	imageDetail?: 'auto' | 'low' | 'high';
}

/**
 * Parameters for prompt creation
 */
export interface PromptParams {
	context: IExecuteFunctions;
	itemIndex: number;
	llm: BaseLanguageModel | BaseChatModel;
	messages?: MessageTemplate[];
	formatInstructions?: string;
	query?: string;
}

/**
 * Parameters for chain execution
 */
export interface ChainExecutionParams {
	context: IExecuteFunctions;
	itemIndex: number;
	query: string;
	llm: BaseLanguageModel;
	outputParser?: N8nOutputParser;
	messages?: MessageTemplate[];
	fallbackLlm?: BaseLanguageModel | null;
}
