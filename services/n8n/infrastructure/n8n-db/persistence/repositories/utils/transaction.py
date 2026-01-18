"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/utils/transaction.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/utils 的工具。导入/依赖:外部:无；内部:@n8n/typeorm；本地:无。导出:无。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected TypeORM Repository/EntityManager usage
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/utils/transaction.ts -> services/n8n/infrastructure/n8n-db/persistence/repositories/utils/transaction.py

import type { EntityManager } from '@n8n/typeorm';

type Tx = EntityManager | null | undefined;

// Wraps a function in a transaction if no EntityManager is passed.
// This allows to use the same function in and out of transactions
// without creating a transaction when already in one.
export async function withTransaction<T>(
	manager: EntityManager,
	trx: Tx,
	run: (em: EntityManager) => Promise<T>,
): Promise<T> {
	if (trx) return await run(trx);

	return await manager.transaction(run);
}
