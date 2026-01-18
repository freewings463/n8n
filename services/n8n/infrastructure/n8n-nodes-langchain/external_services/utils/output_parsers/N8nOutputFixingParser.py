"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/utils/output_parsers/N8nOutputFixingParser.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/utils/output_parsers 的工具。导入/依赖:外部:@langchain/core/…/manager、@langchain/core/…/base、@langchain/core/messages、@langchain/core/output_parsers、@langchain/core/prompts；内部:n8n-workflow；本地:./N8nStructuredOutputParser、../helpers。导出:N8nOutputFixingParser。关键函数/方法:parse、getRetryChain、logAiEvent、result、getFormatInstructions、getSchema。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/utils/output_parsers/N8nOutputFixingParser.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/utils/output_parsers/N8nOutputFixingParser.py

import type { Callbacks } from '@langchain/core/callbacks/manager';
import type { BaseLanguageModel } from '@langchain/core/language_models/base';
import type { AIMessage } from '@langchain/core/messages';
import { BaseOutputParser, OutputParserException } from '@langchain/core/output_parsers';
import type { PromptTemplate } from '@langchain/core/prompts';
import type { ISupplyDataFunctions } from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import type { N8nStructuredOutputParser } from './N8nStructuredOutputParser';
import { logAiEvent } from '../helpers';

export class N8nOutputFixingParser extends BaseOutputParser {
	lc_namespace = ['langchain', 'output_parsers', 'fix'];

	constructor(
		private context: ISupplyDataFunctions,
		private model: BaseLanguageModel,
		private outputParser: N8nStructuredOutputParser,
		private fixPromptTemplate: PromptTemplate,
	) {
		super();
	}

	getRetryChain() {
		return this.fixPromptTemplate.pipe(this.model);
	}

	/**
	 * Attempts to parse the completion string using the output parser.
	 * If the initial parse fails, it tries to fix the output using a retry chain.
	 * @param completion The string to be parsed
	 * @returns The parsed response
	 * @throws Error if both parsing attempts fail
	 */
	async parse(completion: string, callbacks?: Callbacks) {
		const { index } = this.context.addInputData(NodeConnectionTypes.AiOutputParser, [
			[{ json: { action: 'parse', text: completion } }],
		]);

		try {
			// First attempt to parse the completion
			const response = await this.outputParser.parse(completion, callbacks, (e) => {
				if (e instanceof OutputParserException) {
					return e;
				}
				return new OutputParserException(e.message, completion);
			});
			logAiEvent(this.context, 'ai-output-parsed', { text: completion, response });

			this.context.addOutputData(NodeConnectionTypes.AiOutputParser, index, [
				[{ json: { action: 'parse', response } }],
			]);

			return response;
		} catch (error) {
			if (!(error instanceof OutputParserException)) {
				throw error;
			}
			try {
				// Second attempt: use retry chain to fix the output
				const result = (await this.getRetryChain().invoke({
					completion,
					error: error.message,
					instructions: this.getFormatInstructions(),
				})) as AIMessage;

				const resultText = result.content.toString();
				const parsed = await this.outputParser.parse(resultText, callbacks);

				// Add the successfully parsed output to the context
				this.context.addOutputData(NodeConnectionTypes.AiOutputParser, index, [
					[{ json: { action: 'parse', response: parsed } }],
				]);

				return parsed;
			} catch (autoParseError) {
				// If both attempts fail, add the error to the output and throw
				this.context.addOutputData(NodeConnectionTypes.AiOutputParser, index, autoParseError);
				throw autoParseError;
			}
		}
	}

	/**
	 * Method to get the format instructions for the parser.
	 * @returns The format instructions for the parser.
	 */
	getFormatInstructions() {
		return this.outputParser.getFormatInstructions();
	}

	getSchema() {
		return this.outputParser.schema;
	}
}
