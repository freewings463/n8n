"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/fileSearch/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./createStore.operation、./deleteStore.operation、./listStores.operation、./uploadToStore.operation。导出:createStore、deleteStore、listStores、uploadToStore、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/fileSearch/index.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/GoogleGemini/actions/fileSearch/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as createStore from './createStore.operation';
import * as deleteStore from './deleteStore.operation';
import * as listStores from './listStores.operation';
import * as uploadToStore from './uploadToStore.operation';

export { createStore, deleteStore, listStores, uploadToStore };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Create File Search Store',
				value: 'createStore',
				action: 'Create a File Search store',
				description: 'Create a new File Search store for RAG (Retrieval Augmented Generation)',
			},
			{
				name: 'Delete File Search Store',
				value: 'deleteStore',
				action: 'Delete a File Search store',
				description: 'Delete a File Search store',
			},
			{
				name: 'List File Search Stores',
				value: 'listStores',
				action: 'List all File Search stores',
				description: 'List all File Search stores owned by the user',
			},
			{
				name: 'Upload to File Search Store',
				value: 'uploadToStore',
				action: 'Upload a file to a File Search store',
				description:
					'Upload a file to a File Search store for RAG (Retrieval Augmented Generation)',
			},
		],
		default: 'createStore',
		displayOptions: {
			show: {
				resource: ['fileSearch'],
			},
		},
	},
	...createStore.description,
	...deleteStore.description,
	...listStores.description,
	...uploadToStore.description,
];
