"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/OpenAiAssistant/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/OpenAiAssistant 的节点。导入/依赖:外部:@langchain/core/tools、@langchain/openai、zod-to-json-schema；内部:无；本地:无。导出:formatToOpenAIFunction、formatToOpenAITool、formatToOpenAIAssistantTool。关键函数/方法:formatToOpenAIFunction、formatToOpenAITool、formatToOpenAIAssistantTool。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/OpenAiAssistant/utils.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/OpenAiAssistant/utils.py

import type { Tool } from '@langchain/core/tools';
import type { OpenAIClient } from '@langchain/openai';
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
