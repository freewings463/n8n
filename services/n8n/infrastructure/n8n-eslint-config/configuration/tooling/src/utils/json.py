"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/utils/json.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/utils 的工具。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:isJsonParseCall、isJsonStringifyCall。关键函数/方法:isJsonParseCall、isJsonStringifyCall。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/utils/json.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/utils/json.py

import type { TSESTree } from '@typescript-eslint/utils';

export const isJsonParseCall = (node: TSESTree.CallExpression) =>
	node.callee.type === 'MemberExpression' &&
	node.callee.object.type === 'Identifier' &&
	node.callee.object.name === 'JSON' &&
	node.callee.property.type === 'Identifier' &&
	node.callee.property.name === 'parse';

export const isJsonStringifyCall = (node: TSESTree.CallExpression) => {
	const parseArg = node.arguments?.[0];
	return (
		parseArg !== undefined &&
		parseArg.type === 'CallExpression' &&
		parseArg.callee.type === 'MemberExpression' &&
		parseArg.callee.object.type === 'Identifier' &&
		parseArg.callee.object.name === 'JSON' &&
		parseArg.callee.property.type === 'Identifier' &&
		parseArg.callee.property.name === 'stringify'
	);
};
