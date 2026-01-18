"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ConversationalAgent/execute.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:@langchain/community/…/chat_memory、@langchain/core/prompts、@langchain/classic/agents、@utils/helpers、@utils/output_parsers/N8nOutputParser、@utils/schemaParsing 等1项；内部:n8n-workflow；本地:../utils。导出:无。关键函数/方法:conversationalAgentExecute、memory、throwIfToolSchema。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ConversationalAgent/execute.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/agents/ConversationalAgent/execute.py

import type { BaseChatMemory } from '@langchain/community/memory/chat_memory';
import { PromptTemplate } from '@langchain/core/prompts';
import { initializeAgentExecutorWithOptions } from '@langchain/classic/agents';
import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';
import { NodeConnectionTypes, NodeOperationError } from 'n8n-workflow';

import { isChatInstance, getPromptInputByType, getConnectedTools } from '@utils/helpers';
import { getOptionalOutputParser } from '@utils/output_parsers/N8nOutputParser';
import { throwIfToolSchema } from '@utils/schemaParsing';
import { getTracingConfig } from '@utils/tracing';

import { checkForStructuredTools, extractParsedOutput } from '../utils';

export async function conversationalAgentExecute(
	this: IExecuteFunctions,
	nodeVersion: number,
): Promise<INodeExecutionData[][]> {
	this.logger.debug('Executing Conversational Agent');
	const model = await this.getInputConnectionData(NodeConnectionTypes.AiLanguageModel, 0);

	if (!isChatInstance(model)) {
		throw new NodeOperationError(this.getNode(), 'Conversational Agent requires Chat Model');
	}

	const memory = (await this.getInputConnectionData(NodeConnectionTypes.AiMemory, 0)) as
		| BaseChatMemory
		| undefined;

	const tools = await getConnectedTools(this, nodeVersion >= 1.5, true, true);
	const outputParser = await getOptionalOutputParser(this);

	await checkForStructuredTools(tools, this.getNode(), 'Conversational Agent');

	// TODO: Make it possible in the future to use values for other items than just 0
	const options = this.getNodeParameter('options', 0, {}) as {
		systemMessage?: string;
		humanMessage?: string;
		maxIterations?: number;
		returnIntermediateSteps?: boolean;
	};

	const agentExecutor = await initializeAgentExecutorWithOptions(tools, model, {
		// Passing "chat-conversational-react-description" as the agent type
		// automatically creates and uses BufferMemory with the executor.
		// If you would like to override this, you can pass in a custom
		// memory option, but the memoryKey set on it must be "chat_history".
		agentType: 'chat-conversational-react-description',
		memory,
		returnIntermediateSteps: options?.returnIntermediateSteps === true,
		maxIterations: options.maxIterations ?? 10,
		agentArgs: {
			systemMessage: options.systemMessage,
			humanMessage: options.humanMessage,
		},
	});

	const returnData: INodeExecutionData[] = [];

	let prompt: PromptTemplate | undefined;
	if (outputParser) {
		const formatInstructions = outputParser.getFormatInstructions();

		prompt = new PromptTemplate({
			template: '{input}\n{formatInstructions}',
			inputVariables: ['input'],
			partialVariables: { formatInstructions },
		});
	}

	const items = this.getInputData();
	for (let itemIndex = 0; itemIndex < items.length; itemIndex++) {
		try {
			let input;

			if (this.getNode().typeVersion <= 1.2) {
				input = this.getNodeParameter('text', itemIndex) as string;
			} else {
				input = getPromptInputByType({
					ctx: this,
					i: itemIndex,
					inputKey: 'text',
					promptTypeKey: 'promptType',
				});
			}

			if (input === undefined) {
				throw new NodeOperationError(this.getNode(), 'The ‘text parameter is empty.');
			}

			if (prompt) {
				input = (await prompt.invoke({ input })).value;
			}

			const response = await agentExecutor
				.withConfig(getTracingConfig(this))
				.invoke({ input, outputParser });

			if (outputParser) {
				response.output = await extractParsedOutput(this, outputParser, response.output as string);
			}

			returnData.push({ json: response });
		} catch (error) {
			throwIfToolSchema(this, error);

			if (this.continueOnFail()) {
				returnData.push({ json: { error: error.message }, pairedItem: { item: itemIndex } });
				continue;
			}

			throw error;
		}
	}

	return [returnData];
}
