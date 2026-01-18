"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/StopAndError/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/StopAndError 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ErrorHandlerResult、createErrorFromParameters。关键函数/方法:isString、createErrorFromParameters。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/StopAndError/utils.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/StopAndError/utils.py

import type { JsonObject } from 'n8n-workflow';
import { jsonParse } from 'n8n-workflow';

export interface ErrorHandlerResult {
	message: string;
	options?: {
		description?: string;
		type?: string;
		level: 'error';
		metadata?: JsonObject;
	};
}

function isString(value: unknown): value is string {
	return typeof value === 'string' && value.length > 0;
}

export function createErrorFromParameters(
	errorType: 'errorMessage' | 'errorObject',
	errorParameter: string,
): ErrorHandlerResult {
	if (errorType === 'errorMessage') {
		return {
			message: errorParameter,
		};
	} else {
		const errorObject = jsonParse<JsonObject>(errorParameter);

		const errorMessage =
			(isString(errorObject.message) ? errorObject.message : '') ||
			(isString(errorObject.description) ? errorObject.description : '') ||
			(isString(errorObject.error) ? errorObject.error : '') ||
			`Error: ${JSON.stringify(errorObject)}`;

		return {
			message: errorMessage,
			options: {
				description: isString(errorObject.description) ? errorObject.description : undefined,
				type: isString(errorObject.type) ? errorObject.type : undefined,
				level: 'error',
				metadata: errorObject,
			},
		};
	}
}
