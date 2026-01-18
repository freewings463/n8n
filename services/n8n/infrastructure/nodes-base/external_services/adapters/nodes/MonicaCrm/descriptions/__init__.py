"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MonicaCrm/descriptions/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MonicaCrm/descriptions 的入口。导入/依赖:外部:无；内部:无；本地:无。再导出:./ActivityDescription、./CallDescription、./ContactDescription、./ContactFieldDescription 等8项。导出:无。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MonicaCrm/descriptions/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MonicaCrm/descriptions/__init__.py

export * from './ActivityDescription';
export * from './CallDescription';
export * from './ContactDescription';
export * from './ContactFieldDescription';
export * from './ContactTagDescription';
export * from './ConversationDescription';
export * from './ConversationMessageDescription';
export * from './JournalEntryDescription';
export * from './NoteDescription';
export * from './ReminderDescription';
export * from './TagDescription';
export * from './TaskDescription';
