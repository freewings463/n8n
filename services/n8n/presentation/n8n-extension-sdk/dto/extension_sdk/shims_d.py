"""
MIGRATION-META:
  source_path: packages/@n8n/extension-sdk/src/shims.d.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/extension-sdk/src 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。注释目标:/ <reference types="vite/client" />。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Extension SDK contracts/helpers -> presentation/dto
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/extension-sdk/src/shims.d.ts -> services/n8n/presentation/n8n-extension-sdk/dto/extension_sdk/shims_d.py

/// <reference types="vite/client" />
