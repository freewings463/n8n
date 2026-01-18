"""
MIGRATION-META:
  source_path: packages/@n8n/ai-workflow-builder.ee/src/types/connections.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/ai-workflow-builder.ee/src/types 的工作流类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:ConnectionResult、ConnectionValidationResult、ConnectionOperationResult、InferConnectionTypeResult。关键函数/方法:无。用于定义工作流相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - AI workflow builder package -> application/services
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/ai-workflow-builder.ee/src/types/connections.ts -> services/n8n/application/n8n-ai-workflow-builder-ee/services/types/connections.py

import type { INode, NodeConnectionType } from 'n8n-workflow';

/**
 * Result of creating a connection between nodes
 */
export interface ConnectionResult {
	sourceNode: string;
	targetNode: string;
	connectionType: string;
	swapped: boolean;
	message: string;
}

/**
 * Result of connection validation
 */
export interface ConnectionValidationResult {
	valid: boolean;
	error?: string;
	shouldSwap?: boolean;
	swappedSource?: INode;
	swappedTarget?: INode;
}

/**
 * Connection operation result
 */
export interface ConnectionOperationResult {
	success: boolean;
	sourceNode: string;
	targetNode: string;
	connectionType: string;
	swapped: boolean;
	message: string;
	error?: string;
}

/**
 * Result of inferring connection type
 */
export interface InferConnectionTypeResult {
	connectionType?: NodeConnectionType;
	possibleTypes?: NodeConnectionType[];
	requiresSwap?: boolean;
	error?: string;
}
