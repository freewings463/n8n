"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/ToolExecutor/ToolExecutor.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/ToolExecutor 的节点。导入/依赖:外部:@langchain/core/tools、@langchain/classic/agents；内部:n8n-workflow；本地:./utils/executeTool。导出:ToolExecutor。关键函数/方法:execute、toolsInToolkit。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/ToolExecutor/ToolExecutor.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/ToolExecutor/ToolExecutor_node.py

import { Tool, StructuredTool } from '@langchain/core/tools';
import type { Toolkit } from '@langchain/classic/agents';
import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeConnectionTypes, NodeOperationError } from 'n8n-workflow';

import { executeTool } from './utils/executeTool';

export class ToolExecutor implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Tool Executor',
		name: 'toolExecutor',
		version: 1,
		defaults: {
			name: 'Tool Executor',
		},
		hidden: true,
		inputs: [NodeConnectionTypes.Main, NodeConnectionTypes.AiTool],
		outputs: [NodeConnectionTypes.Main],
		properties: [
			{
				displayName: 'Query',
				name: 'query',
				type: 'json',
				default: '{}',
				description: 'Parameters to pass to the tool as JSON or string',
			},
			{
				displayName: 'Tool Name',
				name: 'toolName',
				type: 'string',
				default: '',
				description: 'Name of the tool to execute if the connected tool is a toolkit',
			},
		],
		group: ['transform'],
		description: 'Node to execute tools without an AI Agent',
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const query = this.getNodeParameter('query', 0, {}) as string | object;
		const toolName = this.getNodeParameter('toolName', 0, '') as string;

		let parsedQuery: string | object;

		try {
			parsedQuery = typeof query === 'string' ? JSON.parse(query) : query;
		} catch (error) {
			parsedQuery = query;
		}

		const resultData: INodeExecutionData[] = [];
		const toolInputs = await this.getInputConnectionData(NodeConnectionTypes.AiTool, 0);

		if (!toolInputs || !Array.isArray(toolInputs)) {
			throw new NodeOperationError(this.getNode(), 'No tool inputs found');
		}

		try {
			for (const tool of toolInputs) {
				// Handle toolkits
				if (tool && typeof (tool as Toolkit).getTools === 'function') {
					const toolsInToolkit = (tool as Toolkit).getTools();
					for (const toolkitTool of toolsInToolkit) {
						if (toolkitTool instanceof Tool || toolkitTool instanceof StructuredTool) {
							if (toolName === toolkitTool.name) {
								const result = await executeTool(toolkitTool, parsedQuery);
								resultData.push(result);
							}
						}
					}
				} else {
					// Handle single tool
					if (!toolName || toolName === tool.name) {
						const result = await executeTool(tool, parsedQuery);
						resultData.push(result);
					}
				}
			}
		} catch (error) {
			throw new NodeOperationError(
				this.getNode(),
				`Error executing tool: ${(error as Error).message}`,
			);
		}
		return [resultData];
	}
}
