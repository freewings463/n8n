"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-plugin-community-nodes/src/rules/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-plugin-community-nodes/src/rules 的入口。导入/依赖:外部:@typescript-eslint/utils/ts-eslint；内部:无；本地:./credential-documentation-url.js、./credential-password-field.js、./credential-test-required.js、./icon-validation.js 等7项。导出:rules。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-plugin-community-nodes/src/rules/index.ts -> services/n8n/infrastructure/n8n-eslint-plugin-community-nodes/configuration/tooling/src/rules/__init__.py

import type { AnyRuleModule } from '@typescript-eslint/utils/ts-eslint';

import { CredentialDocumentationUrlRule } from './credential-documentation-url.js';
import { CredentialPasswordFieldRule } from './credential-password-field.js';
import { CredentialTestRequiredRule } from './credential-test-required.js';
import { IconValidationRule } from './icon-validation.js';
import { NoCredentialReuseRule } from './no-credential-reuse.js';
import { NoDeprecatedWorkflowFunctionsRule } from './no-deprecated-workflow-functions.js';
import { NoRestrictedGlobalsRule } from './no-restricted-globals.js';
import { NoRestrictedImportsRule } from './no-restricted-imports.js';
import { NodeUsableAsToolRule } from './node-usable-as-tool.js';
import { PackageNameConventionRule } from './package-name-convention.js';
import { ResourceOperationPatternRule } from './resource-operation-pattern.js';

export const rules = {
	'no-restricted-globals': NoRestrictedGlobalsRule,
	'no-restricted-imports': NoRestrictedImportsRule,
	'credential-password-field': CredentialPasswordFieldRule,
	'no-deprecated-workflow-functions': NoDeprecatedWorkflowFunctionsRule,
	'node-usable-as-tool': NodeUsableAsToolRule,
	'package-name-convention': PackageNameConventionRule,
	'credential-test-required': CredentialTestRequiredRule,
	'no-credential-reuse': NoCredentialReuseRule,
	'icon-validation': IconValidationRule,
	'resource-operation-pattern': ResourceOperationPatternRule,
	'credential-documentation-url': CredentialDocumentationUrlRule,
} satisfies Record<string, AnyRuleModule>;
