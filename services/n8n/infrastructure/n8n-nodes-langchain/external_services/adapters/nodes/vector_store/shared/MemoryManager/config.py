"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vector_store/shared/MemoryManager/config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vector_store/shared 的节点。导入/依赖:外部:无；内部:无；本地:./types。导出:getConfig、mbToBytes、hoursToMs。关键函数/方法:getConfig、mbToBytes、hoursToMs。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vector_store/shared/MemoryManager/config.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vector_store/shared/MemoryManager/config.py

import type { MemoryVectorStoreConfig } from './types';

// Defaults
const DEFAULT_MAX_MEMORY_MB = -1;
const DEFAULT_INACTIVE_TTL_HOURS = -1;

/**
 * Helper function to get the configuration from environment variables
 */
export function getConfig(): MemoryVectorStoreConfig {
	// Get memory limit from env var or use default
	let maxMemoryMB = DEFAULT_MAX_MEMORY_MB;
	if (process.env.N8N_VECTOR_STORE_MAX_MEMORY) {
		const parsed = parseInt(process.env.N8N_VECTOR_STORE_MAX_MEMORY, 10);
		if (!isNaN(parsed)) {
			maxMemoryMB = parsed;
		}
	}

	// Get TTL from env var or use default
	let ttlHours = DEFAULT_INACTIVE_TTL_HOURS;
	if (process.env.N8N_VECTOR_STORE_TTL_HOURS) {
		const parsed = parseInt(process.env.N8N_VECTOR_STORE_TTL_HOURS, 10);
		if (!isNaN(parsed)) {
			ttlHours = parsed;
		}
	}

	return {
		maxMemoryMB,
		ttlHours,
	};
}

/**
 * Convert memory size from MB to bytes
 */
export function mbToBytes(mb: number): number {
	// -1 - "unlimited"
	if (mb <= 0) return -1;
	return mb * 1024 * 1024;
}

/**
 * Convert TTL from hours to milliseconds
 */
export function hoursToMs(hours: number): number {
	// -1 - "disabled"
	if (hours <= 0) return -1;
	return hours * 60 * 60 * 1000;
}
