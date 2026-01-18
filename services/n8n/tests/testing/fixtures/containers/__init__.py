"""
MIGRATION-META:
  source_path: packages/testing/containers/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/containers 的入口。导入/依赖:外部:无；内部:无；本地:无。再导出:./performance-plans。导出:createN8NStack、type LogEntry、type GiteaHelper。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。注释目标:n8n Test Containers / This package provides container management utilities for n8n testing.。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (containers harness) -> tests/fixtures/containers
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/containers/index.ts -> services/n8n/tests/testing/fixtures/containers/__init__.py

/**
 * n8n Test Containers
 *
 * This package provides container management utilities for n8n testing.
 * Services are accessed via n8nContainer.services.* in tests.
 */

// Stack orchestration - primary public API
export { createN8NStack } from './stack';
export type { N8NConfig, N8NStack } from './stack';

// Performance plans (CLI-only)
export * from './performance-plans';

// Types used externally by tests
export { type LogEntry } from './services/observability';
export { type GiteaHelper } from './services/gitea';
