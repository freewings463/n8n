"""
MIGRATION-META:
  source_path: packages/@n8n/db/src/subscribers/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/db/src/subscribers 的入口。导入/依赖:外部:无；内部:无；本地:./user-subscriber。导出:subscribers。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package @n8n/db defaulted to persistence infrastructure
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/db/src/subscribers/index.ts -> services/n8n/infrastructure/n8n-db/persistence/subscribers/__init__.py

import { UserSubscriber } from './user-subscriber';

export const subscribers = {
	UserSubscriber,
};
