"""
MIGRATION-META:
  source_path: packages/core/src/instance-settings/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/src/instance-settings 的入口。导入/依赖:外部:无；内部:无；本地:无。导出:InstanceSettings。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Instance settings wiring -> infrastructure/configuration
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/instance-settings/index.ts -> services/n8n/infrastructure/core/configuration/instance_settings/__init__.py

export { InstanceSettings } from './instance-settings';
