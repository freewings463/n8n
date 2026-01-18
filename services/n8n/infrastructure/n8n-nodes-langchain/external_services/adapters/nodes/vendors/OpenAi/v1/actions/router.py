"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v1/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的路由。导入/依赖:外部:无；内部:无；本地:./assistant、./audio、./file、./image 等3项。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v1/actions/router.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/v1/actions/router.py

import {
	NodeOperationError,
	type IExecuteFunctions,
	type INodeExecutionData,
	NodeApiError,
} from 'n8n-workflow';

import * as assistant from './assistant';
import * as audio from './audio';
import * as file from './file';
import * as image from './image';
import type { OpenAiType } from './node.type';
import * as text from './text';
import { getCustomErrorMessage } from '../../helpers/error-handling';

export async function router(this: IExecuteFunctions) {
	const returnData: INodeExecutionData[] = [];

	const items = this.getInputData();
	const resource = this.getNodeParameter<OpenAiType>('resource', 0);
	const operation = this.getNodeParameter('operation', 0);

	const openAiTypeData = {
		resource,
		operation,
	} as OpenAiType;

	let execute;
	switch (openAiTypeData.resource) {
		case 'assistant':
			execute = assistant[openAiTypeData.operation].execute;
			break;
		case 'audio':
			execute = audio[openAiTypeData.operation].execute;
			break;
		case 'file':
			execute = file[openAiTypeData.operation].execute;
			break;
		case 'image':
			execute = image[openAiTypeData.operation].execute;
			break;
		case 'text':
			execute = text[openAiTypeData.operation].execute;
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

			if (error instanceof NodeApiError) {
				// If the error is a rate limit error, we want to handle it differently
				const errorCode: string | undefined = (error.cause as any)?.error?.error?.code;
				if (errorCode) {
					const customErrorMessage = getCustomErrorMessage(errorCode);
					if (customErrorMessage) {
						error.message = customErrorMessage;
					}
				}

				error.context = {
					itemIndex: i,
				};

				throw error;
			}

			throw new NodeOperationError(this.getNode(), error, {
				itemIndex: i,
				description: error.description,
			});
		}
	}

	return [returnData];
}
