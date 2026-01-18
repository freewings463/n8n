"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/tsup.config.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain 的配置。导入/依赖:外部:tsup；内部:无；本地:无。导出:无。关键函数/方法:无。用于集中定义该模块配置项与默认值，供其他模块读取。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Integration package tooling/config file
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/tsup.config.ts -> services/n8n/infrastructure/n8n-nodes-langchain/configuration/tooling/tsup_config.py

import { defineConfig } from 'tsup';

export default defineConfig({
	entry: ['{credentials,nodes,test,types,utils}/**/*.ts', '!**/*.d.ts', '!**/*.test.ts'],
	format: ['cjs'],
	clean: true,
	dts: false,
	bundle: false,
	sourcemap: true,
	silent: true,
});
