"""
MIGRATION-META:
  source_path: packages/cli/src/deduplication/index.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/deduplication 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./deduplication-helper。导出:getDataDeduplicationService。关键函数/方法:getDataDeduplicationService。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Deduplication helpers -> application/services/deduplication
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/deduplication/index.ts -> services/n8n/application/cli/services/deduplication/__init__.py

import { type IDataDeduplicator } from 'n8n-workflow';

import { DeduplicationHelper } from './deduplication-helper';

export function getDataDeduplicationService(): IDataDeduplicator {
	return new DeduplicationHelper();
}
