"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/mcp/McpClientTool/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/mcp/McpClientTool 的节点。导入/依赖:外部:@langchain/core/tools、@modelcontextprotocol/sdk/…/index.js 等4项；内部:n8n-workflow；本地:./types 等1项。导出:getSelectedTools、getErrorDescriptionFromToolCall、createCallTool、mcpToolToDynamicTool、McpToolkit。关键函数/方法:getSelectedTools、getErrorDescriptionFromToolCall、errorMessage、async、handleError、onError 等1项。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/mcp/McpClientTool/utils.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/mcp/McpClientTool/utils.py

import { DynamicStructuredTool, type DynamicStructuredToolInput } from '@langchain/core/tools';
import type { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { CompatibilityCallToolResultSchema } from '@modelcontextprotocol/sdk/types.js';
import { Toolkit } from '@langchain/classic/agents';
import { type IDataObject } from 'n8n-workflow';
import { z } from 'zod';

import { convertJsonSchemaToZod } from '@utils/schemaParsing';

import type { McpToolIncludeMode } from './types';
import type { McpTool } from '../shared/types';

export function getSelectedTools({
	mode,
	includeTools,
	excludeTools,
	tools,
}: {
	mode: McpToolIncludeMode;
	includeTools?: string[];
	excludeTools?: string[];
	tools: McpTool[];
}) {
	switch (mode) {
		case 'selected': {
			if (!includeTools?.length) return tools;
			const include = new Set(includeTools);
			return tools.filter((tool) => include.has(tool.name));
		}
		case 'except': {
			const except = new Set(excludeTools ?? []);
			return tools.filter((tool) => !except.has(tool.name));
		}
		case 'all':
		default:
			return tools;
	}
}

export const getErrorDescriptionFromToolCall = (result: unknown): string | undefined => {
	if (result && typeof result === 'object') {
		if ('content' in result && Array.isArray(result.content)) {
			const errorMessage = (result.content as Array<{ type: 'text'; text: string }>).find(
				(content) => content && typeof content === 'object' && typeof content.text === 'string',
			)?.text;
			return errorMessage;
		} else if ('toolResult' in result && typeof result.toolResult === 'string') {
			return result.toolResult;
		}
		if ('message' in result && typeof result.message === 'string') {
			return result.message;
		}
	}

	return undefined;
};

export const createCallTool =
	(name: string, client: Client, timeout: number, onError: (error: string) => void) =>
	async (args: IDataObject) => {
		let result: Awaited<ReturnType<Client['callTool']>>;

		function handleError(error: unknown) {
			const errorDescription =
				getErrorDescriptionFromToolCall(error) ?? `Failed to execute tool "${name}"`;
			onError(errorDescription);
			return errorDescription;
		}

		try {
			result = await client.callTool({ name, arguments: args }, CompatibilityCallToolResultSchema, {
				timeout,
			});
		} catch (error) {
			return handleError(error);
		}

		if (result.isError) {
			return handleError(result);
		}

		if (result.toolResult !== undefined) {
			return result.toolResult;
		}

		if (result.content !== undefined) {
			return result.content;
		}

		return result;
	};

export function mcpToolToDynamicTool(
	tool: McpTool,
	onCallTool: DynamicStructuredToolInput['func'],
): DynamicStructuredTool {
	const rawSchema = convertJsonSchemaToZod(tool.inputSchema);

	// Ensure we always have an object schema for structured tools
	const objectSchema =
		rawSchema instanceof z.ZodObject ? rawSchema : z.object({ value: rawSchema });

	return new DynamicStructuredTool({
		name: tool.name,
		description: tool.description ?? '',
		schema: objectSchema,
		func: onCallTool,
		metadata: { isFromToolkit: true },
	});
}

export class McpToolkit extends Toolkit {
	constructor(public tools: DynamicStructuredTool[]) {
		super();
	}
}
