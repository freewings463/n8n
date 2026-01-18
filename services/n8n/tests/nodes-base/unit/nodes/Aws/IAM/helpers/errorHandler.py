"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/IAM/helpers/errorHandler.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/IAM 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./constants、./types。导出:无。关键函数/方法:mapErrorToResponse、handleError。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/IAM/helpers/errorHandler.ts -> services/n8n/tests/nodes-base/unit/nodes/Aws/IAM/helpers/errorHandler.py

import type {
	JsonObject,
	IDataObject,
	IExecuteSingleFunctions,
	IN8nHttpFullResponse,
	INodeExecutionData,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

import { ERROR_DESCRIPTIONS } from './constants';
import type { AwsError, ErrorMessage } from './types';

function mapErrorToResponse(errorCode: string, errorMessage: string): ErrorMessage | undefined {
	const isUser = /user/i.test(errorMessage);
	const isGroup = /group/i.test(errorMessage);

	switch (errorCode) {
		case 'EntityAlreadyExists':
			if (isUser) {
				return {
					message: errorMessage,
					description: ERROR_DESCRIPTIONS.EntityAlreadyExists.User,
				};
			}
			if (isGroup) {
				return {
					message: errorMessage,
					description: ERROR_DESCRIPTIONS.EntityAlreadyExists.Group,
				};
			}
			break;

		case 'NoSuchEntity':
			if (isUser) {
				return {
					message: errorMessage,
					description: ERROR_DESCRIPTIONS.NoSuchEntity.User,
				};
			}
			if (isGroup) {
				return {
					message: errorMessage,
					description: ERROR_DESCRIPTIONS.NoSuchEntity.Group,
				};
			}
			break;

		case 'DeleteConflict':
			return {
				message: errorMessage,
				description: ERROR_DESCRIPTIONS.DeleteConflict.Default,
			};
	}

	return undefined;
}

export async function handleError(
	this: IExecuteSingleFunctions,
	data: INodeExecutionData[],
	response: IN8nHttpFullResponse,
): Promise<INodeExecutionData[]> {
	const statusCode = String(response.statusCode);

	if (!statusCode.startsWith('4') && !statusCode.startsWith('5')) {
		return data;
	}

	const responseBody = response.body as IDataObject;
	const error = responseBody.Error as AwsError;

	if (!error) {
		throw new NodeApiError(this.getNode(), response as unknown as JsonObject);
	}

	const specificError = mapErrorToResponse(error.Code, error.Message);

	if (specificError) {
		throw new NodeApiError(this.getNode(), response as unknown as JsonObject, specificError);
	} else {
		throw new NodeApiError(this.getNode(), response as unknown as JsonObject, {
			message: error.Code,
			description: error.Message,
		});
	}
}
