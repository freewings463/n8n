"""
MIGRATION-META:
  source_path: packages/workflow/vitest.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/workflow 的工作流配置。导入/依赖:外部:无；内部:@n8n/vitest-config/node；本地:无。导出:无。关键函数/方法:无。用于集中定义工作流配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Package workflow tooling/config file
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/workflow/vitest.config.ts -> services/n8n/infrastructure/workflow/configuration/tooling/vitest_config.py

import { createVitestConfig } from '@n8n/vitest-config/node';

export default createVitestConfig({ include: ['test/**/*.test.ts'] });
