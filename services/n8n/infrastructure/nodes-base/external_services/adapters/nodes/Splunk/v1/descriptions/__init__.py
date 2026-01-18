"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Splunk/v1/descriptions/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Splunk/v1 的入口。导入/依赖:外部:无；内部:无；本地:无。再导出:./FiredAlertDescription、./SearchConfigurationDescription、./SearchJobDescription、./SearchResultDescription 等1项。导出:无。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Splunk/v1/descriptions/index.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Splunk/v1/descriptions/__init__.py

export * from './FiredAlertDescription';
export * from './SearchConfigurationDescription';
export * from './SearchJobDescription';
export * from './SearchResultDescription';
export * from './UserDescription';
