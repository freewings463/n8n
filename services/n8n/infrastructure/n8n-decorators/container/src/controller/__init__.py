"""
MIGRATION-META:
  source_path: packages/@n8n/decorators/src/controller/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/decorators/src/controller 的入口。导入/依赖:外部:无；内部:无；本地:无。导出:Body、Query、Param、RestController、RootLevelController、Get、Post、Put 等9项。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - DI/container wiring -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/decorators/src/controller/index.ts -> services/n8n/infrastructure/n8n-decorators/container/src/controller/__init__.py

export { Body, Query, Param } from './args';
export { RestController } from './rest-controller';
export { RootLevelController } from './root-level-controller';
export { Get, Post, Put, Patch, Delete, Head, Options } from './route';
export { Middleware } from './middleware';
export { ControllerRegistryMetadata } from './controller-registry-metadata';
export { Licensed } from './licensed';
export { GlobalScope, ProjectScope } from './scoped';
export type { AccessScope, Controller, RateLimit, StaticRouterMetadata } from './types';
