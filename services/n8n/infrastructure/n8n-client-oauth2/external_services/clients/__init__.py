"""
MIGRATION-META:
  source_path: packages/@n8n/client-oauth2/src/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/client-oauth2/src 的OAuth入口。导入/依赖:外部:无；内部:无；本地:无。导出:ClientOAuth2、ClientOAuth2Token。关键函数/方法:无。用于汇总导出并完成OAuth模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Package @n8n/client-oauth2 treated as external service client library
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/client-oauth2/src/index.ts -> services/n8n/infrastructure/n8n-client-oauth2/external_services/clients/__init__.py

export type { ClientOAuth2Options, ClientOAuth2RequestObject } from './client-oauth2';
export { ClientOAuth2 } from './client-oauth2';
export type { ClientOAuth2TokenData } from './client-oauth2-token';
export { ClientOAuth2Token } from './client-oauth2-token';
export type * from './types';
