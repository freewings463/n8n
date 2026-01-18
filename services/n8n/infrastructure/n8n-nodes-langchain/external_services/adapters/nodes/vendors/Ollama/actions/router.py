"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/Ollama/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/Ollama 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./image、./node.type、./text。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/Ollama/actions/router.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/Ollama/actions/router.py

import { NodeOperationError, type IExecuteFunctions, type INodeExecutionData } from 'n8n-workflow';

import * as image from './image';
import type { OllamaType } from './node.type';
import * as text from './text';

export async function router(this: IExecuteFunctions) {
	const returnData: INodeExecutionData[] = [];

	const items = this.getInputData();
	const resource = this.getNodeParameter('resource', 0);
	const operation = this.getNodeParameter('operation', 0);

	const ollamaTypeData = {
		resource,
		operation,
	} as OllamaType;

	let execute;
	switch (ollamaTypeData.resource) {
		case 'image':
			execute = image[ollamaTypeData.operation].execute;
			break;
		case 'text':
			execute = text[ollamaTypeData.operation].execute;
			break;
		default:
			throw new NodeOperationError(this.getNode(), `The resource "${resource}" is not supported!`);
	}

	for (let i = 0; i < items.length; i++) {
		try {
			const responseData = await execute.call(this, i);
			returnData.push.apply(returnData, responseData);
		} catch (error) {
			if (this.continueOnFail()) {
				returnData.push({ json: { error: error.message }, pairedItem: { item: i } });
				continue;
			}

			throw new NodeOperationError(this.getNode(), error, {
				itemIndex: i,
				description: error.description,
			});
		}
	}

	return [returnData];
}
