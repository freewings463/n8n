"""
MIGRATION-META:
  source_path: packages/cli/src/auth/index.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/auth 的认证入口。导入/依赖:外部:无；内部:无；本地:无。再导出:./methods/email。导出:无。关键函数/方法:无。用于汇总导出并完成认证模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Authentication helpers/use-cases -> application/services/auth
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/auth/index.ts -> services/n8n/application/cli/services/auth/__init__.py

export * from './methods/email';
