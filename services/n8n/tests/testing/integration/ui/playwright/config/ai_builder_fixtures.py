"""
MIGRATION-META:
  source_path: packages/testing/playwright/config/ai-builder-fixtures.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/playwright/config 的配置。导入/依赖:外部:无；内部:无；本地:../Types。导出:workflowBuilderEnabledRequirements。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (playwright) -> tests/integration/ui/playwright
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/playwright/config/ai-builder-fixtures.ts -> services/n8n/tests/testing/integration/ui/playwright/config/ai_builder_fixtures.py

import type { TestRequirements } from '../Types';

/**
 * Requirements for enabling the AI workflow builder feature.
 * These tests use the real Anthropic API for workflow generation,
 * requiring N8N_AI_ANTHROPIC_KEY to be set in the environment.
 */
export const workflowBuilderEnabledRequirements: TestRequirements = {
	config: {
		settings: {
			aiAssistant: { enabled: true, setup: true },
			aiBuilder: { enabled: true, setup: true },
		},
		features: {
			aiAssistant: true,
			aiBuilder: true,
		},
	},
};
