"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/AzureCosmosDb/helpers/errorHandler.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/AzureCosmosDb 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./interfaces。导出:ErrorMap。关键函数/方法:handleError。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/AzureCosmosDb/helpers/errorHandler.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/AzureCosmosDb/helpers/errorHandler.py

import type {
	IExecuteSingleFunctions,
	IN8nHttpFullResponse,
	INodeExecutionData,
	JsonObject,
} from 'n8n-workflow';
import { jsonParse, NodeApiError } from 'n8n-workflow';

import type { IErrorResponse } from './interfaces';

export const ErrorMap = {
	Container: {
		Conflict: {
			getMessage: (id: string) => `Container "${id}" already exists.`,
			description: "Use a unique value for 'ID' and try again.",
		},
		NotFound: {
			getMessage: (id: string) => `Container "${id}" was not found.`,
			description: "Double-check the value in the parameter 'Container' and try again.",
		},
	},
	Item: {
		NotFound: {
			getMessage: (id: string) => `Item "${id}" was not found.`,
			description:
				"Double-check the values in the parameter 'Item' and 'Partition Key' (if applicable) and try again.",
		},
	},
};

export async function handleError(
	this: IExecuteSingleFunctions,
	data: INodeExecutionData[],
	response: IN8nHttpFullResponse,
): Promise<INodeExecutionData[]> {
	if (String(response.statusCode).startsWith('4') || String(response.statusCode).startsWith('5')) {
		const resource = this.getNodeParameter('resource') as string;
		const error = response.body as IErrorResponse;
		let errorMessage = error.message;

		let errorDetails: string[] | undefined = undefined;

		if (resource === 'container') {
			if (error.code === 'Conflict') {
				const newContainerValue = this.getNodeParameter('containerCreate') as string;
				throw new NodeApiError(this.getNode(), error as unknown as JsonObject, {
					message: ErrorMap.Container.Conflict.getMessage(newContainerValue ?? 'Unknown'),
					description: ErrorMap.Container.Conflict.description,
				});
			}
			if (error.code === 'NotFound') {
				const containerValue = this.getNodeParameter('container', undefined, {
					extractValue: true,
				}) as string;
				throw new NodeApiError(this.getNode(), error as unknown as JsonObject, {
					message: ErrorMap.Container.NotFound.getMessage(containerValue ?? 'Unknown'),
					description: ErrorMap.Container.NotFound.description,
				});
			}
		} else if (resource === 'item') {
			if (error.code === 'NotFound') {
				const itemValue = this.getNodeParameter('item', undefined, {
					extractValue: true,
				}) as string;
				throw new NodeApiError(this.getNode(), error as unknown as JsonObject, {
					message: ErrorMap.Item.NotFound.getMessage(itemValue ?? 'Unknown'),
					description: ErrorMap.Item.NotFound.description,
				});
			}
		}

		try {
			// Certain error responses have nested Message
			errorMessage = jsonParse<{
				message: string;
			}>(errorMessage).message;
		} catch {}

		const match = errorMessage.match(/Message: ({.*?})/);
		if (match?.[1]) {
			try {
				errorDetails = jsonParse<{
					Errors: string[];
				}>(match[1]).Errors;
			} catch {}
		}

		if (errorDetails && errorDetails.length > 0) {
			throw new NodeApiError(this.getNode(), error as unknown as JsonObject, {
				message: error.code,
				description: errorDetails.join('\n'),
			});
		} else {
			throw new NodeApiError(this.getNode(), error as unknown as JsonObject, {
				message: error.code,
				description: error.message,
			});
		}
	}
	return data;
}
