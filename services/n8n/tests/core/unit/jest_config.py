"""
MIGRATION-META:
  source_path: packages/core/jest.config.js
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core 的配置。导入/依赖:外部:jest；内部:无；本地:../../jest.config。导出:无。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/jest.config.js -> services/n8n/tests/core/unit/jest_config.py

/** @type {import('jest').Config} */
module.exports = {
	...require('../../jest.config'),
	globalSetup: '<rootDir>/test/setup.ts',
	setupFilesAfterEnv: ['<rootDir>/test/setup-mocks.ts'],
};
