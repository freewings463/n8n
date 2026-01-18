"""
MIGRATION-META:
  source_path: packages/@n8n/stylelint-config/jest.config.cjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/stylelint-config 的配置。导入/依赖:外部:jest；内部:无；本地:../../jest.config。导出:无。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/stylelint-config/jest.config.cjs -> services/n8n/tests/n8n-stylelint-config/unit/jest_config.py

/** @type {import('jest').Config} */
module.exports = {
	...require('../../../jest.config'),
	transform: {
		'^.+\\.ts$': ['ts-jest', { isolatedModules: false }],
	},
};
