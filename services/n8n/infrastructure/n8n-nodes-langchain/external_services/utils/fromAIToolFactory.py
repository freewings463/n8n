"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/utils/fromAIToolFactory.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/utils 的工具。导入/依赖:外部:@langchain/core/…/manager、@langchain/core/tools、zod；内部:n8n-workflow；本地:无。导出:ToolFunc、CreateToolOptions、extractFromAIParameters、createZodSchemaFromArgs、createToolFromNode。关键函数/方法:extractFromAIParameters、traverseNodeParameters、createZodSchemaFromArgs、createToolFromNode。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package defaulted to infrastructure/external_services
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/utils/fromAIToolFactory.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/utils/fromAIToolFactory.py

import type { CallbackManagerForToolRun } from '@langchain/core/callbacks/manager';
import { DynamicStructuredTool, DynamicTool } from '@langchain/core/tools';
import type { FromAIArgument, IDataObject, INode, INodeParameters } from 'n8n-workflow';
import { generateZodSchema, traverseNodeParameters } from 'n8n-workflow';
import { z } from 'zod';

export type ToolFunc = (
	query: string | IDataObject,
	runManager?: CallbackManagerForToolRun,
) => Promise<string | IDataObject | IDataObject[]>;

export interface CreateToolOptions {
	name: string;
	description: string;
	func: ToolFunc;
	/**
	 * Extra arguments to include in the structured tool schema.
	 * These are added after extracting $fromAI parameters from node parameters.
	 */
	extraArgs?: FromAIArgument[];
}

/**
 * Extracts $fromAI parameters from node parameters and returns unique arguments.
 */
export function extractFromAIParameters(nodeParameters: INodeParameters): FromAIArgument[] {
	const collectedArguments: FromAIArgument[] = [];
	traverseNodeParameters(nodeParameters, collectedArguments);

	const uniqueArgsMap = new Map<string, FromAIArgument>();
	for (const arg of collectedArguments) {
		uniqueArgsMap.set(arg.key, arg);
	}

	return Array.from(uniqueArgsMap.values());
}

/**
 * Creates a Zod schema from $fromAI arguments.
 */
export function createZodSchemaFromArgs(args: FromAIArgument[]): z.ZodObject<z.ZodRawShape> {
	const schemaObj = args.reduce((acc: Record<string, z.ZodTypeAny>, placeholder) => {
		acc[placeholder.key] = generateZodSchema(placeholder);
		return acc;
	}, {});

	return z.object(schemaObj).required();
}

/**
 * Creates a DynamicStructuredTool if node has $fromAI parameters,
 * otherwise falls back to a simple DynamicTool.
 *
 * This is useful for creating AI agent tools that can extract parameters
 * from node configuration using $fromAI expressions.
 */
export function createToolFromNode(
	node: INode,
	options: CreateToolOptions,
): DynamicStructuredTool | DynamicTool {
	const { name, description, func, extraArgs = [] } = options;

	const collectedArguments = extractFromAIParameters(node.parameters);

	// If there are no $fromAI arguments and no extra args, fallback to simple tool
	if (collectedArguments.length === 0 && extraArgs.length === 0) {
		return new DynamicTool({ name, description, func });
	}

	// Combine collected arguments with extra arguments
	const allArguments = [...collectedArguments, ...extraArgs];
	const schema = createZodSchemaFromArgs(allArguments);

	return new DynamicStructuredTool({ schema, name, description, func });
}
