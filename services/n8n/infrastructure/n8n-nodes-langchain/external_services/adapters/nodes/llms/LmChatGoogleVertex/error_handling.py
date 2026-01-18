"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/llms/LmChatGoogleVertex/error-handling.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/llms/LmChatGoogleVertex 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:ErrorLike、ErrorContext、makeErrorFromStatus。关键函数/方法:makeErrorFromStatus。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/llms/LmChatGoogleVertex/error-handling.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/llms/LmChatGoogleVertex/error_handling.py

export interface ErrorLike {
	message?: string;
	description?: string;
}

export interface ErrorContext {
	modelName?: string;
}

export function makeErrorFromStatus(statusCode: number, context?: ErrorContext): ErrorLike {
	const errorMessages: Record<number, ErrorLike> = {
		403: {
			message: 'Unauthorized for this project',
			description:
				'Check your Google Cloud project ID, that your credential has access to that project and that billing is enabled',
		},
		404: {
			message: context?.modelName
				? `No model found called '${context.modelName}'`
				: 'No model found',
		},
	};

	return errorMessages[statusCode];
}
