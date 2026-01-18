"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-plugin-community-nodes/src/utils/rule-creator.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-plugin-community-nodes/src/utils 的工具。导入/依赖:外部:@typescript-eslint/utils；内部:无；本地:无。导出:createRule。关键函数/方法:无。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-plugin-community-nodes/src/utils/rule-creator.ts -> services/n8n/infrastructure/n8n-eslint-plugin-community-nodes/configuration/tooling/src/utils/rule_creator.py

import { ESLintUtils } from '@typescript-eslint/utils';

const REPO_URL = 'https://github.com/n8n-io/n8n';
const DOCS_PATH = 'blob/master/packages/@n8n/eslint-plugin-community-nodes/docs/rules';

export const createRule = ESLintUtils.RuleCreator((name) => `${REPO_URL}/${DOCS_PATH}/${name}.md`);
