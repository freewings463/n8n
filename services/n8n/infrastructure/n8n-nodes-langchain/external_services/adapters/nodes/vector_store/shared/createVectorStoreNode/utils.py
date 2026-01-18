"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/shared/createVectorStoreNode/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/shared 的节点。导入/依赖:外部:@langchain/core/vectorstores；内部:n8n-workflow；本地:./constants、./types。导出:transformDescriptionForOperationMode、isUpdateSupported、getOperationModeOptions。关键函数/方法:transformDescriptionForOperationMode。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/shared/createVectorStoreNode/utils.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/shared/createVectorStoreNode/utils.py

import type { VectorStore } from '@langchain/core/vectorstores';
import type { INodeProperties, INodePropertyOptions } from 'n8n-workflow';

import { DEFAULT_OPERATION_MODES, OPERATION_MODE_DESCRIPTIONS } from './constants';
import type { NodeOperationMode, VectorStoreNodeConstructorArgs } from './types';

/**
 * Transforms field descriptions to show only for specific operation modes
 * This function adds displayOptions to each field to make it appear only for specified modes
 */
export function transformDescriptionForOperationMode(
	fields: INodeProperties[],
	mode: NodeOperationMode | NodeOperationMode[],
): INodeProperties[] {
	return fields.map((field) => ({
		...field,
		displayOptions: { show: { mode: Array.isArray(mode) ? mode : [mode] } },
	}));
}

/**
 * Checks if the update operation is supported for a specific vector store
 * A vector store supports updates if it explicitly includes 'update' in its operationModes
 */
export function isUpdateSupported<T extends VectorStore>(
	args: VectorStoreNodeConstructorArgs<T>,
): boolean {
	return args.meta.operationModes?.includes('update') ?? false;
}

/**
 * Returns the operation mode options enabled for a specific vector store
 * Filters the full list of operation modes based on what's enabled for this vector store
 */
export function getOperationModeOptions<T extends VectorStore>(
	args: VectorStoreNodeConstructorArgs<T>,
): INodePropertyOptions[] {
	const enabledOperationModes = args.meta.operationModes ?? DEFAULT_OPERATION_MODES;

	return OPERATION_MODE_DESCRIPTIONS.filter(({ value }) =>
		enabledOperationModes.includes(value as NodeOperationMode),
	);
}
