"""
MIGRATION-META:
  source_path: packages/@n8n/eslint-config/src/rules/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/eslint-config/src/rules 的入口。导入/依赖:外部:@typescript-eslint/utils/ts-eslint；内部:无；本地:./no-json-parse-json-stringify.js、./no-uncaught-json-parse.js、./no-unneeded-backticks.js、./no-unused-param-catch-clause.js 等14项。导出:rules。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Tooling package (lint/test config) -> infrastructure/configuration/tooling
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/eslint-config/src/rules/index.ts -> services/n8n/infrastructure/n8n-eslint-config/configuration/tooling/src/rules/__init__.py

import { NoJsonParseJsonStringifyRule } from './no-json-parse-json-stringify.js';
import { NoUncaughtJsonParseRule } from './no-uncaught-json-parse.js';
import { NoUnneededBackticksRule } from './no-unneeded-backticks.js';
import { NoUnusedParamInCatchClauseRule } from './no-unused-param-catch-clause.js';
import { NoUselessCatchThrowRule } from './no-useless-catch-throw.js';
import { NoSkippedTestsRule } from './no-skipped-tests.js';
import { NoInterpolationInRegularStringRule } from './no-interpolation-in-regular-string.js';
import { NoPlainErrorsRule } from './no-plain-errors.js';
import { NoDynamicImportTemplateRule } from './no-dynamic-import-template.js';
import { MisplacedN8nTypeormImportRule } from './misplaced-n8n-typeorm-import.js';
import { NoTypeUnsafeEventEmitterRule } from './no-type-unsafe-event-emitter.js';
import { NoUntypedConfigClassFieldRule } from './no-untyped-config-class-field.js';
import { NoTopLevelRelativeImportsInBackendModuleRule } from './no-top-level-relative-imports-in-backend-module.js';
import { NoConstructorInBackendModuleRule } from './no-constructor-in-backend-module.js';
import type { AnyRuleModule } from '@typescript-eslint/utils/ts-eslint';
import { NoArgumentSpreadRule } from './no-argument-spread.js';
import { NoInternalPackageImportRule } from './no-internal-package-import.js';
import { NoImportEnterpriseEditionRule } from './no-import-enterprise-edition.js';
import { NoTypeOnlyImportInDiRule } from './no-type-only-import-in-di.js';

export const rules = {
	'no-uncaught-json-parse': NoUncaughtJsonParseRule,
	'no-json-parse-json-stringify': NoJsonParseJsonStringifyRule,
	'no-unneeded-backticks': NoUnneededBackticksRule,
	'no-unused-param-in-catch-clause': NoUnusedParamInCatchClauseRule,
	'no-useless-catch-throw': NoUselessCatchThrowRule,
	'no-skipped-tests': NoSkippedTestsRule,
	'no-interpolation-in-regular-string': NoInterpolationInRegularStringRule,
	'no-plain-errors': NoPlainErrorsRule,
	'no-dynamic-import-template': NoDynamicImportTemplateRule,
	'misplaced-n8n-typeorm-import': MisplacedN8nTypeormImportRule,
	'no-type-unsafe-event-emitter': NoTypeUnsafeEventEmitterRule,
	'no-untyped-config-class-field': NoUntypedConfigClassFieldRule,
	'no-top-level-relative-imports-in-backend-module': NoTopLevelRelativeImportsInBackendModuleRule,
	'no-constructor-in-backend-module': NoConstructorInBackendModuleRule,
	'no-argument-spread': NoArgumentSpreadRule,
	'no-internal-package-import': NoInternalPackageImportRule,
	'no-import-enterprise-edition': NoImportEnterpriseEditionRule,
	'no-type-only-import-in-di': NoTypeOnlyImportInDiRule,
} satisfies Record<string, AnyRuleModule>;
