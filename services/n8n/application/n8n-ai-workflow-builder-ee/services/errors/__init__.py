"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/errors/index.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/errors 的工作流入口。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:NodeNotFoundError、NodeTypeNotFoundError、ConnectionError、LLMServiceError、ValidationError、ParameterUpdateError、ParameterTooLargeError、WorkflowStateError 等1项。关键函数/方法:无。用于汇总导出并完成工作流模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/errors/index.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/errors/__init__.py

import { OperationalError, UnexpectedError } from 'n8n-workflow';
import type { OperationalErrorOptions, UnexpectedErrorOptions } from 'n8n-workflow';

/**
 * Base error class for AI Workflow Builder specific errors
 */
export abstract class AiWorkflowBuilderError extends Error {
	constructor(message: string, options?: ErrorOptions) {
		super(message, options);
		this.name = this.constructor.name;
	}
}

/**
 * Error thrown when a node is not found in the workflow
 */
export class NodeNotFoundError extends OperationalError {
	constructor(nodeId: string, nodeType?: string, options?: OperationalErrorOptions) {
		super(`Node with ID "${nodeId}" not found in workflow`, {
			...options,
			tags: {
				...options?.tags,
				nodeId,
				nodeType,
			},
			shouldReport: false,
		});
	}
}

/**
 * Error thrown when a node type is not found in the available node types
 */
export class NodeTypeNotFoundError extends OperationalError {
	constructor(nodeType: string, options?: OperationalErrorOptions) {
		super(`Node type "${nodeType}" not found`, {
			...options,
			tags: {
				...options?.tags,
				nodeType,
			},
			shouldReport: false,
		});
	}
}

/**
 * Error thrown when there's an issue with node connections
 */
export class ConnectionError extends OperationalError {
	constructor(
		message: string,
		options?: OperationalErrorOptions & {
			fromNodeId?: string;
			toNodeId?: string;
			connectionType?: string;
		},
	) {
		super(message, {
			...options,
			tags: {
				...options?.tags,
				fromNodeId: options?.fromNodeId,
				toNodeId: options?.toNodeId,
				connectionType: options?.connectionType,
			},
			shouldReport: false,
		});
	}
}

/**
 * Error thrown when the LLM service fails
 */
export class LLMServiceError extends OperationalError {
	constructor(
		message: string,
		options?: OperationalErrorOptions & { llmModel?: string; statusCode?: number },
	) {
		super(message, {
			...options,
			tags: {
				...options?.tags,
				llmModel: options?.llmModel,
				statusCode: options?.statusCode,
			},
			shouldReport: true,
		});
	}
}

/**
 * Error thrown when validation fails
 */
export class ValidationError extends OperationalError {
	constructor(
		message: string,
		options?: OperationalErrorOptions & { field?: string; value?: unknown },
	) {
		super(message, {
			...options,
			tags: {
				...options?.tags,
				field: options?.field,
			},
			extra: {
				...options?.extra,
				value: options?.value,
			},
			shouldReport: false,
		});
	}
}

/**
 * Error thrown when parameter update fails
 */
export class ParameterUpdateError extends OperationalError {
	constructor(
		message: string,
		options?: OperationalErrorOptions & { nodeId?: string; nodeType: string; parameter?: string },
	) {
		super(message, {
			...options,
			tags: {
				...options?.tags,
				nodeId: options?.nodeId,
				nodeType: options?.nodeType,
				parameter: options?.parameter,
			},
			shouldReport: false,
		});
	}
}

/**
 * Error thrown when parameter value is too large to retrieve
 */
export class ParameterTooLargeError extends OperationalError {
	constructor(
		message: string,
		options?: OperationalErrorOptions & { nodeId?: string; parameter?: string; maxSize?: number },
	) {
		super(message, {
			...options,
			tags: {
				...options?.tags,
				nodeId: options?.nodeId,
				parameter: options?.parameter,
				maxSize: options?.maxSize,
			},
			shouldReport: false,
		});
	}
}

/**
 * Error thrown when workflow state is invalid
 */
export class WorkflowStateError extends UnexpectedError {
	constructor(message: string, options?: UnexpectedErrorOptions) {
		super(message, {
			...options,
			shouldReport: true,
		});
	}
}

/**
 * Error thrown when tool execution fails unexpectedly
 */
export class ToolExecutionError extends UnexpectedError {
	constructor(message: string, options?: UnexpectedErrorOptions & { toolName?: string }) {
		super(message, {
			...options,
			shouldReport: true,
			tags: {
				...options?.tags,
				toolName: options?.toolName,
			},
		});
	}
}
