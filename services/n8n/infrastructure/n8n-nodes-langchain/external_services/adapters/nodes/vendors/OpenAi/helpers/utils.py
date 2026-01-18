"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/helpers/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:@langchain/core/messages、@langchain/core/tools 等3项；内部:n8n-workflow；本地:无。导出:formatToOpenAIFunction、formatToOpenAITool、formatToOpenAIAssistantTool、formatToOpenAIResponsesTool。关键函数/方法:formatToOpenAIFunction、formatToOpenAITool、formatToOpenAIAssistantTool、requireStrict、formatToOpenAIResponsesTool 等2项。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/helpers/utils.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/helpers/utils.py

import type { BaseMessage } from '@langchain/core/messages';
import type { Tool } from '@langchain/core/tools';
import type { OpenAIClient } from '@langchain/openai';
import type { BufferWindowMemory } from '@langchain/classic/memory';
import { isObjectEmpty } from 'n8n-workflow';
import { zodToJsonSchema } from 'zod-to-json-schema';

// Copied from langchain(`langchain/src/tools/convert_to_openai.ts`)
// since these functions are not exported

/**
 * Formats a `Tool` instance into a format that is compatible
 * with OpenAI's ChatCompletionFunctions. It uses the `zodToJsonSchema`
 * function to convert the schema of the tool into a JSON
 * schema, which is then used as the parameters for the OpenAI function.
 */
export function formatToOpenAIFunction(
	tool: Tool,
): OpenAIClient.Chat.ChatCompletionCreateParams.Function {
	return {
		name: tool.name,
		description: tool.description,
		parameters: zodToJsonSchema(tool.schema),
	};
}

export function formatToOpenAITool(tool: Tool): OpenAIClient.Chat.ChatCompletionTool {
	const schema = zodToJsonSchema(tool.schema);
	return {
		type: 'function',
		function: {
			name: tool.name,
			description: tool.description,
			parameters: schema,
		},
	};
}

export function formatToOpenAIAssistantTool(tool: Tool): OpenAIClient.Beta.AssistantTool {
	return {
		type: 'function',
		function: {
			name: tool.name,
			description: tool.description,
			parameters: zodToJsonSchema(tool.schema),
		},
	};
}

const requireStrict = (schema: any) => {
	if (!schema.required) {
		return false;
	}
	// when strict:true, Responses API requires `required` to be present and all properties to be included
	if (schema.properties) {
		const propertyNames = Object.keys(schema.properties);
		const somePropertyMissingFromRequired = propertyNames.some(
			(propertyName) => !schema.required.includes(propertyName),
		);
		const requireStrict = !somePropertyMissingFromRequired;
		return requireStrict;
	}
	return false;
};

export function formatToOpenAIResponsesTool(tool: Tool): OpenAIClient.Responses.FunctionTool {
	const schema = zodToJsonSchema(tool.schema) as any;
	const strict = requireStrict(schema);

	// when strict:true, Responses API requires `additionalProperties` either to be true/false or an object with properties
	const isAdditionalPropertiesEmpty =
		schema.additionalProperties &&
		typeof schema.additionalProperties === 'object' &&
		isObjectEmpty(schema.additionalProperties);
	if (isAdditionalPropertiesEmpty && strict) {
		schema.additionalProperties = false;
	}

	return {
		type: 'function',
		name: tool.name,
		parameters: schema,
		strict,
		description: tool.description,
	};
}

export async function getChatMessages(memory: BufferWindowMemory): Promise<BaseMessage[]> {
	return (await memory.loadMemoryVariables({}))[memory.memoryKey] as BaseMessage[];
}
