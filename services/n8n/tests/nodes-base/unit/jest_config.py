"""
MIGRATION-META:
  source_path: packages/nodes-base/jest.config.js
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base 的配置。导入/依赖:外部:jest；内部:无；本地:../../jest.config。导出:无。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。注释目标:Avoid tests failing because of difference between local and GitHub actions timezone。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/jest.config.js -> services/n8n/tests/nodes-base/unit/jest_config.py

// Avoid tests failing because of difference between local and GitHub actions timezone
process.env.TZ = 'UTC';

/** @type {import('jest').Config} */
module.exports = {
	...require('../../jest.config'),
	collectCoverageFrom: ['credentials/**/*.ts', 'nodes/**/*.ts', 'utils/**/*.ts'],
	globalSetup: '<rootDir>/test/globalSetup.ts',
	setupFilesAfterEnv: ['jest-expect-message', '<rootDir>/test/setup.ts'],
};
