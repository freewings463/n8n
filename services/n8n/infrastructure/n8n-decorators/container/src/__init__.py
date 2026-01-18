"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src 的入口。导入/依赖:外部:无；内部:无；本地:无。再导出:./controller、./command、./execution-lifecycle、./context-establishment 等6项。导出:Debounce、Memoized、Redactable、Timed。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/index.ts -> services/n8n/infrastructure/n8n-decorators/container/src/__init__.py

export * from './controller';
export * from './command';
export { Debounce } from './debounce';
export * from './execution-lifecycle';
export { Memoized } from './memoized';
export * from './context-establishment';
export * from './credential-resolver';
export * from './module';
export * from './multi-main';
export * from './pubsub';
export { Redactable } from './redactable';
export * from './shutdown';
export * from './module/module-metadata';
export type { TimedOptions } from './timed';
export { Timed } from './timed';
