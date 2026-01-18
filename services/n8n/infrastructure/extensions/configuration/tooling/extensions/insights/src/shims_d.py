"""
MIGRATION-META:
  source_path: packages/extensions/insights/src/shims.d.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/extensions/src 的Insights类型。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:无。用于定义Insights相关类型/结构约束，供多模块共享。注释目标:/ <reference types="vite/client" />。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Extensions package -> infrastructure/configuration/tooling/extensions
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/extensions/insights/src/shims.d.ts -> services/n8n/infrastructure/extensions/configuration/tooling/extensions/insights/src/shims_d.py

/// <reference types="vite/client" />
