"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/tools/ToolWorkflow/v2/ToolWorkflowV2.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/tools/ToolWorkflow 的工作流节点。导入/依赖:外部:@langchain/core/tools；内部:n8n-workflow；本地:./methods、./utils/WorkflowToolService、./versionDescription。导出:ToolWorkflowV2。关键函数/方法:execute、getTool、supplyData。用于实现 n8n 工作流节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/tools/ToolWorkflow/v2/ToolWorkflowV2.node.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/tools/ToolWorkflow/v2/ToolWorkflowV2_node.py

import type { DynamicStructuredTool, DynamicTool } from '@langchain/core/tools';

import type {
	INodeTypeBaseDescription,
	ISupplyDataFunctions,
	SupplyData,
	INodeType,
	INodeTypeDescription,
	IExecuteFunctions,
	INodeExecutionData,
} from 'n8n-workflow';
import { nodeNameToToolName, NodeOperationError } from 'n8n-workflow';

import { localResourceMapping } from './methods';
import { WorkflowToolService } from './utils/WorkflowToolService';
import { versionDescription } from './versionDescription';

async function getTool(
	ctx: ISupplyDataFunctions | IExecuteFunctions,
	enableLogging: boolean,
	itemIndex: number,
): Promise<DynamicTool | DynamicStructuredTool> {
	const node = ctx.getNode();
	const { typeVersion } = node;
	const returnAllItems = typeVersion > 2;

	const workflowToolService = new WorkflowToolService(ctx, { returnAllItems });
	const name =
		typeVersion <= 2.1 ? (ctx.getNodeParameter('name', 0) as string) : nodeNameToToolName(node);
	const description = ctx.getNodeParameter('description', 0) as string;

	return await workflowToolService.createTool({
		ctx,
		name,
		description,
		itemIndex,
		manualLogging: enableLogging,
	});
}

export class ToolWorkflowV2 implements INodeType {
	description: INodeTypeDescription;

	constructor(baseDescription: INodeTypeBaseDescription) {
		this.description = {
			...baseDescription,
			...versionDescription,
		};
	}

	methods = {
		localResourceMapping,
	};

	async supplyData(this: ISupplyDataFunctions, itemIndex: number): Promise<SupplyData> {
		return { response: await getTool(this, true, itemIndex) };
	}

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();

		const response: INodeExecutionData[] = [];
		for (let itemIndex = 0; itemIndex < this.getInputData().length; itemIndex++) {
			const item = items[itemIndex];
			const tool = await getTool(this, false, itemIndex);

			if (item === undefined) {
				continue;
			}

			try {
				const result = await tool.invoke(item.json);

				// When manualLogging is false, tool.invoke returns INodeExecutionData[]
				// We need to spread these into the response array
				if (Array.isArray(result)) {
					response.push(...result);
				} else {
					// Fallback for unexpected types (shouldn't happen with manualLogging=false)
					response.push({
						json: { response: result },
						pairedItem: { item: itemIndex },
					});
				}
			} catch (error) {
				// Catch schema validation errors (ToolInputParsingException) and other errors
				// Re-throw as NodeOperationError with itemIndex for better error context
				const errorMessage = error instanceof Error ? error.message : 'Unknown error';
				throw new NodeOperationError(this.getNode(), errorMessage, { itemIndex });
			}
		}

		return [response];
	}
}
