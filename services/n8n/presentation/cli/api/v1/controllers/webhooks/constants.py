"""
MIGRATION-META:
  source_path: packages/cli/src/webhooks/constants.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/webhooks 的Webhook模块。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:authAllowlistedNodes。关键函数/方法:无。用于承载Webhook实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Webhook HTTP entry -> presentation/api/v1/controllers/webhooks
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/webhooks/constants.ts -> services/n8n/presentation/cli/api/v1/controllers/webhooks/constants.py

import { CHAT_TRIGGER_NODE_TYPE } from 'n8n-workflow';

export const authAllowlistedNodes = new Set([CHAT_TRIGGER_NODE_TYPE]);
