"""
MIGRATION-META:
  source_path: packages/@n8n/extension-sdk/tsdown.config.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/@n8n/extension-sdk 的配置。导入/依赖:外部:tsdown；内部:无；本地:无。导出:无。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Extension SDK contracts/helpers -> presentation/dto
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/extension-sdk/tsdown.config.ts -> services/n8n/presentation/n8n-extension-sdk/dto/extension_sdk/tsdown_config.py

import { defineConfig } from 'tsdown';

// eslint-disable-next-line import-x/no-default-export
export default defineConfig([
	{
		clean: false,
		entry: ['src/*.ts', '!src/*.test.ts', '!src/*.d.ts', '!src/__tests__/**/*'],
		outDir: 'dist',
		format: ['cjs', 'esm'],
		dts: true,
		sourcemap: true,
		tsconfig: 'tsconfig.common.json',
		hash: false,
	},
	{
		clean: false,
		entry: [
			'src/backend/**/*.ts',
			'!src/backend/**/*.test.ts',
			'!src/backend/**/*.d.ts',
			'!src/backend/__tests__/**/*',
		],
		outDir: 'dist/backend',
		format: ['cjs', 'esm'],
		dts: true,
		sourcemap: true,
		tsconfig: 'tsconfig.backend.json',
		hash: false,
	},
	{
		clean: false,
		entry: [
			'src/frontend/**/*.ts',
			'!src/frontend/**/*.test.ts',
			'!src/frontend/**/*.d.ts',
			'!src/frontend/__tests__/**/*',
		],
		outDir: 'dist/frontend',
		format: ['cjs', 'esm'],
		dts: true,
		sourcemap: true,
		tsconfig: 'tsconfig.frontend.json',
		hash: false,
	},
]);
