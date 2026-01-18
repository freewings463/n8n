"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/task-broker/auth/task-broker-auth.schema.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/task-runners/task-broker/auth 的认证模块。导入/依赖:外部:zod；内部:无；本地:无。导出:taskBrokerAuthRequestBodySchema。关键函数/方法:无。用于承载认证实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/task-broker/auth/task-broker-auth.schema.ts -> services/n8n/application/cli/services/task-runners/task-broker/auth/task_broker_auth_schema.py

import { z } from 'zod';

export const taskBrokerAuthRequestBodySchema = z.object({
	token: z.string().min(1),
});
