"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/shared/MemoryManager/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/shared 的类型。导入/依赖:外部:@langchain/core/documents、@langchain/classic/…/memory；内部:无；本地:无。导出:MemoryVectorStoreConfig、VectorStoreMetadata、StoreStats、VectorStoreStats、IMemoryCalculator、IStoreCleanupService。关键函数/方法:estimateBatchSize、calculateVectorStoreSize、cleanupInactiveStores、cleanupOldestStores。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/shared/MemoryManager/types.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/shared/MemoryManager/types.py

import type { Document } from '@langchain/core/documents';
import type { MemoryVectorStore } from '@langchain/classic/vectorstores/memory';

/**
 * Configuration options for the memory vector store
 */
export interface MemoryVectorStoreConfig {
	/**
	 * Maximum memory size in MB, -1 to disable
	 */
	maxMemoryMB: number;

	/**
	 * TTL for inactive stores in hours, -1 to disable
	 */
	ttlHours: number;
}

/**
 * Vector store metadata for tracking usage
 */
export interface VectorStoreMetadata {
	size: number;
	createdAt: Date;
	lastAccessed: Date;
}

/**
 * Per-store statistics for reporting
 */
export interface StoreStats {
	sizeBytes: number;
	sizeMB: number;
	percentOfTotal: number;
	vectors: number;
	createdAt: string;
	lastAccessed: string;
	inactive?: boolean;
	inactiveForHours?: number;
}

/**
 * Overall vector store statistics
 */
export interface VectorStoreStats {
	totalSizeBytes: number;
	totalSizeMB: number;
	percentOfLimit: number;
	maxMemoryMB: number;
	storeCount: number;
	inactiveStoreCount: number;
	ttlHours: number;
	stores: Record<string, StoreStats>;
}

/**
 * Service for calculating memory usage
 */
export interface IMemoryCalculator {
	estimateBatchSize(documents: Document[]): number;
	calculateVectorStoreSize(vectorStore: MemoryVectorStore): number;
}

/**
 * Service for cleaning up vector stores
 */
export interface IStoreCleanupService {
	cleanupInactiveStores(): void;
	cleanupOldestStores(requiredBytes: number): void;
}
