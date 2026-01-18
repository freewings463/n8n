"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/chains/InformationExtractor/processItem.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/chains/InformationExtractor 的节点。导入/依赖:外部:@langchain/core/…/base、@langchain/core/messages、@langchain/core/prompts、@langchain/classic/output_parsers、@utils/tracing；内部:n8n-workflow；本地:./constants。导出:无。关键函数/方法:processItem。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/chains/InformationExtractor/processItem.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/chains/InformationExtractor/processItem.py

import type { BaseLanguageModel } from '@langchain/core/language_models/base';
import { HumanMessage } from '@langchain/core/messages';
import { ChatPromptTemplate, SystemMessagePromptTemplate } from '@langchain/core/prompts';
import type { OutputFixingParser } from '@langchain/classic/output_parsers';
import { NodeOperationError, type IExecuteFunctions } from 'n8n-workflow';

import { getTracingConfig } from '@utils/tracing';

import { SYSTEM_PROMPT_TEMPLATE } from './constants';

export async function processItem(
	ctx: IExecuteFunctions,
	itemIndex: number,
	llm: BaseLanguageModel,
	parser: OutputFixingParser<object>,
) {
	const input = ctx.getNodeParameter('text', itemIndex) as string;
	if (!input?.trim()) {
		throw new NodeOperationError(ctx.getNode(), `Text for item ${itemIndex} is not defined`, {
			itemIndex,
		});
	}
	const inputPrompt = new HumanMessage(input);

	const options = ctx.getNodeParameter('options', itemIndex, {}) as {
		systemPromptTemplate?: string;
	};

	const systemPromptTemplate = SystemMessagePromptTemplate.fromTemplate(
		`${options.systemPromptTemplate ?? SYSTEM_PROMPT_TEMPLATE}
{format_instructions}`,
	);

	const messages = [
		await systemPromptTemplate.format({
			format_instructions: parser.getFormatInstructions(),
		}),
		inputPrompt,
	];
	const prompt = ChatPromptTemplate.fromMessages(messages);
	const chain = prompt.pipe(llm).pipe(parser).withConfig(getTracingConfig(ctx));

	return await chain.invoke(messages);
}
