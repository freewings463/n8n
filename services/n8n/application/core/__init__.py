"""
MIGRATION-META:
  source_path: packages/core/src/index.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src 的入口。导入/依赖:外部:无；内部:无；本地:./node-execute-functions。再导出:./binary-data、./constants、./credentials、./data-deduplication-service 等9项。导出:WorkflowHasIssuesError、NodeExecuteFunctions、CUSTOM_NODES_PACKAGE_NAME。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core package entrypoint -> application/__init__.py
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/index.ts -> services/n8n/application/core/__init__.py

import * as NodeExecuteFunctions from './node-execute-functions';

export * from './binary-data';
export * from './constants';
export * from './credentials';
export * from './data-deduplication-service';
export * from './encryption';
export * from './errors';
export * from './execution-engine';
export * from './html-sandbox';
export * from './instance-settings';
export * from './nodes-loader';
export * from './utils';
export * from './http-proxy';
export { WorkflowHasIssuesError } from './errors/workflow-has-issues.error';

export type * from './interfaces';
export * from './node-execute-functions';
export { NodeExecuteFunctions };

export { CUSTOM_NODES_PACKAGE_NAME } from './nodes-loader/constants';
