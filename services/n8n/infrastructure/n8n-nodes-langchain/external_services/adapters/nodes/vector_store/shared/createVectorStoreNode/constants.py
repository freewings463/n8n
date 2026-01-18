"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/shared/createVectorStoreNode/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/shared 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./types。导出:DEFAULT_OPERATION_MODES、OPERATION_MODE_DESCRIPTIONS。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/shared/createVectorStoreNode/constants.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/shared/createVectorStoreNode/constants.py

import { NodeConnectionTypes } from 'n8n-workflow';
import type { INodePropertyOptions } from 'n8n-workflow';

import type { NodeOperationMode } from './types';

export const DEFAULT_OPERATION_MODES: NodeOperationMode[] = [
	'load',
	'insert',
	'retrieve',
	'retrieve-as-tool',
];

export const OPERATION_MODE_DESCRIPTIONS: INodePropertyOptions[] = [
	{
		name: 'Get Many',
		value: 'load',
		description: 'Get many ranked documents from vector store for query',
		action: 'Get ranked documents from vector store',
	},
	{
		name: 'Insert Documents',
		value: 'insert',
		description: 'Insert documents into vector store',
		action: 'Add documents to vector store',
	},
	{
		name: 'Retrieve Documents (As Vector Store for Chain/Tool)',
		value: 'retrieve',
		description: 'Retrieve documents from vector store to be used as vector store with AI nodes',
		action: 'Retrieve documents for Chain/Tool as Vector Store',
		outputConnectionType: NodeConnectionTypes.AiVectorStore,
	},
	{
		name: 'Retrieve Documents (As Tool for AI Agent)',
		value: 'retrieve-as-tool',
		description: 'Retrieve documents from vector store to be used as tool with AI nodes',
		action: 'Retrieve documents for AI Agent as Tool',
		outputConnectionType: NodeConnectionTypes.AiTool,
	},
	{
		name: 'Update Documents',
		value: 'update',
		description: 'Update documents in vector store by ID',
		action: 'Update vector store documents',
	},
];
