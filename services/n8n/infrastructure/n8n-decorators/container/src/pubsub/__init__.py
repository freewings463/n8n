"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/pubsub/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src/pubsub 的入口。导入/依赖:外部:无；内部:无；本地:无。导出:PubSubMetadata、OnPubSubEvent。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/pubsub/index.ts -> services/n8n/infrastructure/n8n-decorators/container/src/pubsub/__init__.py

export type { PubSubEventName } from './pubsub-metadata';
export { PubSubMetadata } from './pubsub-metadata';
export { OnPubSubEvent } from './on-pubsub-event';
