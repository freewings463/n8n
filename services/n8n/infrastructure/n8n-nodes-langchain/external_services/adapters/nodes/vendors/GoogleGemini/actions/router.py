"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./audio、./document、./file、./fileSearch 等4项。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/router.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/GoogleGemini/actions/router.py

import { NodeOperationError, type IExecuteFunctions, type INodeExecutionData } from 'n8n-workflow';

import * as audio from './audio';
import * as document from './document';
import * as file from './file';
import * as fileSearch from './fileSearch';
import * as image from './image';
import type { GoogleGeminiType } from './node.type';
import * as text from './text';
import * as video from './video';

export async function router(this: IExecuteFunctions) {
	const returnData: INodeExecutionData[] = [];

	const items = this.getInputData();
	const resource = this.getNodeParameter('resource', 0);
	const operation = this.getNodeParameter('operation', 0);

	const googleGeminiTypeData = {
		resource,
		operation,
	} as GoogleGeminiType;

	let execute;
	switch (googleGeminiTypeData.resource) {
		case 'audio':
			execute = audio[googleGeminiTypeData.operation].execute;
			break;
		case 'document':
			execute = document[googleGeminiTypeData.operation].execute;
			break;
		case 'file':
			execute = file[googleGeminiTypeData.operation].execute;
			break;
		case 'fileSearch':
			execute = fileSearch[googleGeminiTypeData.operation].execute;
			break;
		case 'image':
			execute = image[googleGeminiTypeData.operation].execute;
			break;
		case 'text':
			execute = text[googleGeminiTypeData.operation].execute;
			break;
		case 'video':
			execute = video[googleGeminiTypeData.operation].execute;
			break;
		default:
			throw new NodeOperationError(
				this.getNode(),
				`The operation "${operation}" is not supported!`,
			);
	}

	for (let i = 0; i < items.length; i++) {
		try {
			const responseData = await execute.call(this, i);
			returnData.push(...responseData);
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
