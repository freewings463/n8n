"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/chains/ChainSummarization/helpers.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/chains/ChainSummarization 的工具。导入/依赖:外部:@langchain/core/prompts、@langchain/classic/chains；内部:无；本地:无。导出:getChainPromptsArgs。关键函数/方法:getChainPromptsArgs。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/chains/ChainSummarization/helpers.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/chains/ChainSummarization/helpers.py

import { PromptTemplate } from '@langchain/core/prompts';
import type { SummarizationChainParams } from '@langchain/classic/chains';
interface ChainTypeOptions {
	combineMapPrompt?: string;
	prompt?: string;
	refinePrompt?: string;
	refineQuestionPrompt?: string;
}

export function getChainPromptsArgs(
	type: 'stuff' | 'map_reduce' | 'refine',
	options: ChainTypeOptions,
) {
	const chainArgs: SummarizationChainParams = {
		type,
	};
	// Map reduce prompt override
	if (type === 'map_reduce') {
		const mapReduceArgs = chainArgs as SummarizationChainParams & {
			type: 'map_reduce';
		};
		if (options.combineMapPrompt) {
			mapReduceArgs.combineMapPrompt = new PromptTemplate({
				template: options.combineMapPrompt,
				inputVariables: ['text'],
			});
		}
		if (options.prompt) {
			mapReduceArgs.combinePrompt = new PromptTemplate({
				template: options.prompt,
				inputVariables: ['text'],
			});
		}
	}

	// Stuff prompt override
	if (type === 'stuff') {
		const stuffArgs = chainArgs as SummarizationChainParams & {
			type: 'stuff';
		};
		if (options.prompt) {
			stuffArgs.prompt = new PromptTemplate({
				template: options.prompt,
				inputVariables: ['text'],
			});
		}
	}

	// Refine prompt override
	if (type === 'refine') {
		const refineArgs = chainArgs as SummarizationChainParams & {
			type: 'refine';
		};

		if (options.refinePrompt) {
			refineArgs.refinePrompt = new PromptTemplate({
				template: options.refinePrompt,
				inputVariables: ['existing_answer', 'text'],
			});
		}

		if (options.refineQuestionPrompt) {
			refineArgs.questionPrompt = new PromptTemplate({
				template: options.refineQuestionPrompt,
				inputVariables: ['text'],
			});
		}
	}

	return chainArgs;
}
