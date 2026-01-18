"""
MIGRATION-META:
  source_path: packages/testing/playwright/fixtures/capabilities.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/fixtures 的模块。导入/依赖:外部:无；内部:n8n-containers/stack；本地:无。导出:CAPABILITIES、Capability、INFRASTRUCTURE_MODES、CONTAINER_ONLY_CAPABILITIES、CONTAINER_ONLY_MODES。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/fixtures/capabilities.ts -> services/n8n/tests/testing/integration/ui/playwright/fixtures/capabilities.py

import type { N8NConfig } from 'n8n-containers/stack';

/**
 * Capability definitions for `test.use({ capability: 'email' })`.
 * Add `@capability:X` tag to tests for orchestration grouping.
 *
 * Maps capability names to service registry keys.
 * Note: task-runner is always enabled, no capability needed.
 */
export const CAPABILITIES = {
	email: { services: ['mailpit'] },
	proxy: { services: ['proxy'] },
	'source-control': { services: ['gitea'] },
	oidc: { services: ['keycloak'] },
	observability: { services: ['victoriaLogs', 'victoriaMetrics', 'vector'] },
} as const satisfies Record<string, Partial<N8NConfig>>;

export type Capability = keyof typeof CAPABILITIES;

/**
 * Infrastructure modes (`@mode:X` tags). Most tests run against ALL modes via projects.
 * Use @mode:X only for tests requiring specific infrastructure.
 */
export const INFRASTRUCTURE_MODES = ['postgres', 'queue', 'multi-main'] as const;

// Used by playwright-projects.ts to filter container-only tests in local mode
export const CONTAINER_ONLY_CAPABILITIES = Object.keys(CAPABILITIES) as Capability[];
export const CONTAINER_ONLY_MODES = INFRASTRUCTURE_MODES;
