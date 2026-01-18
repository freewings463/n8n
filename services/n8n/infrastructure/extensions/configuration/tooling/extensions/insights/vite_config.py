"""
MIGRATION-META:
  source_path: packages/extensions/insights/vite.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/extensions/insights 的Insights配置。导入/依赖:外部:vite、@vitejs/plugin-vue、vite-plugin-dts、vitest/config；内部:无；本地:无。导出:无。关键函数/方法:vue、dts。用于集中定义Insights配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Extensions package -> infrastructure/configuration/tooling/extensions
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/extensions/insights/vite.config.ts -> services/n8n/infrastructure/extensions/configuration/tooling/extensions/insights/vite_config.py

import { resolve } from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import dts from 'vite-plugin-dts';
import { configDefaults as vitestConfig } from 'vitest/config';

const cwd = process.cwd();

export default defineConfig({
	plugins: [
		vue(),
		dts({
			rollupTypes: true,
			tsconfigPath: resolve(cwd, 'tsconfig.frontend.json'),
		}),
	],
	build: {
		emptyOutDir: false,
		outDir: resolve(cwd, 'dist', 'frontend'),
		lib: {
			entry: resolve(cwd, 'src', 'frontend', 'index.ts'),
			name: 'n8nFrontEndSdk',
			fileName: 'index',
		},
		rollupOptions: {
			external: ['vue'],
			output: {
				preserveModules: false,
				globals: {
					vue: 'Vue',
				},
			},
		},
	},
	test: {
		globals: true,
		environment: 'jsdom',
		setupFiles: ['src/__tests__/setup.ts'],
		include: ['src/**/*.spec.ts'],
		exclude: vitestConfig.exclude,
	},
});
