"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/configs/node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/configs 的模块。导入/依赖:外部:typescript-eslint、globals；内部:无；本地:./base.js。导出:nodeConfig。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/configs/node.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/configs/node.py

import tseslint from 'typescript-eslint';
import globals from 'globals';
import { baseConfig } from './base.js';

export const nodeConfig = tseslint.config(baseConfig, {
	languageOptions: {
		ecmaVersion: 2024,
		globals: globals.node,
	},
});
