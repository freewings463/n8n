"""
MIGRATION-META:
  source_path: packages/cli/src/modules/breaking-changes/rules/index.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/breaking-changes/rules 的入口。导入/依赖:外部:无；内部:无；本地:./v2。导出:allRules、type RuleInstances。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/breaking-changes/rules/index.ts -> services/n8n/application/cli/services/modules/breaking-changes/rules/__init__.py

import { v2Rules } from './v2';

const allRules = [...v2Rules];
type RuleConstructors = (typeof allRules)[number];
type RuleInstances = InstanceType<RuleConstructors>;

export { allRules, type RuleInstances };
