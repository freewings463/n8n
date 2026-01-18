"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/plugins.d.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:无。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/plugins.d.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/plugins_d.py

declare module 'eslint-plugin-lodash';
