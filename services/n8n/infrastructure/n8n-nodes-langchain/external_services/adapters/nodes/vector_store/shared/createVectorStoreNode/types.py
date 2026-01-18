"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/shared/createVectorStoreNode/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/shared 的类型。导入/依赖:外部:@langchain/core/documents、@langchain/core/embeddings、@langchain/core/vectorstores；内部:无；本地:无。导出:NodeOperationMode、NodeMeta、VectorStoreNodeConstructorArgs。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/shared/createVectorStoreNode/types.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/shared/createVectorStoreNode/types.py

import type { Document } from '@langchain/core/documents';
import type { Embeddings } from '@langchain/core/embeddings';
import type { VectorStore } from '@langchain/core/vectorstores';
import type {
	IExecuteFunctions,
	INodeCredentialDescription,
	INodeProperties,
	ILoadOptionsFunctions,
	INodeListSearchResult,
	Icon,
	ISupplyDataFunctions,
	ThemeIconColor,
	IDataObject,
	NodeParameterValueType,
} from 'n8n-workflow';

export type NodeOperationMode = 'insert' | 'load' | 'retrieve' | 'update' | 'retrieve-as-tool';

export interface NodeMeta {
	displayName: string;
	name: string;
	hidden?: boolean;
	description: string;
	docsUrl: string;
	icon: Icon;
	iconColor?: ThemeIconColor;
	credentials?: INodeCredentialDescription[];
	operationModes?: NodeOperationMode[];
	categories?: string[];
	subcategories?: Record<string, string[]>;
}

export interface VectorStoreNodeConstructorArgs<T extends VectorStore = VectorStore> {
	meta: NodeMeta;
	methods?: {
		listSearch?: {
			[key: string]: (
				this: ILoadOptionsFunctions,
				filter?: string,
				paginationToken?: string,
			) => Promise<INodeListSearchResult>;
		};
		actionHandler?: {
			[functionName: string]: (
				this: ILoadOptionsFunctions,
				payload: IDataObject | string | undefined,
			) => Promise<NodeParameterValueType>;
		};
	};

	sharedFields: INodeProperties[];
	insertFields?: INodeProperties[];
	loadFields?: INodeProperties[];
	retrieveFields?: INodeProperties[];
	updateFields?: INodeProperties[];

	/**
	 * Function to populate the vector store with documents
	 * Used during the 'insert' operation mode
	 */
	populateVectorStore: (
		context: IExecuteFunctions | ISupplyDataFunctions,
		embeddings: Embeddings,
		documents: Array<Document<Record<string, unknown>>>,
		itemIndex: number,
	) => Promise<void>;

	/**
	 * Function to get the vector store client
	 * This function is called for all operation modes
	 */
	getVectorStoreClient: (
		context: IExecuteFunctions | ISupplyDataFunctions,
		filter: Record<string, never> | undefined,
		embeddings: Embeddings,
		itemIndex: number,
	) => Promise<T>;

	/**
	 * Optional function to release resources associated with the vector store client
	 * Called after the vector store operations are complete
	 */
	releaseVectorStoreClient?: (vectorStore: T) => void;
}
