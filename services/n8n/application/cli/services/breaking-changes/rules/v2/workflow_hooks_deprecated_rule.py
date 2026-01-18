"""
MIGRATION-META:
  source_path: packages/cli/src/modules/breaking-changes/rules/v2/workflow-hooks-deprecated.rule.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/breaking-changes/rules 的工作流模块。导入/依赖:外部:无；内部:@n8n/di；本地:../../types。导出:WorkflowHooksDeprecatedRule。关键函数/方法:getMetadata、detect。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/breaking-changes/rules/v2/workflow-hooks-deprecated.rule.ts -> services/n8n/application/cli/services/breaking-changes/rules/v2/workflow_hooks_deprecated_rule.py

import { Service } from '@n8n/di';

import type {
	BreakingChangeRuleMetadata,
	IBreakingChangeInstanceRule,
	InstanceDetectionReport,
} from '../../types';
import { BreakingChangeCategory } from '../../types';

@Service()
export class WorkflowHooksDeprecatedRule implements IBreakingChangeInstanceRule {
	id: string = 'workflow-hooks-deprecated-v2';

	getMetadata(): BreakingChangeRuleMetadata {
		return {
			version: 'v2',
			title: 'Deprecated frontend workflow hooks',
			description:
				'The hooks workflow.activeChange and workflow.activeChangeCurrent are deprecated and replaced by workflow.published',
			category: BreakingChangeCategory.instance,
			severity: 'low',
			documentationUrl:
				'https://docs.n8n.io/2-0-breaking-changes/#deprecated-frontend-workflow-hooks',
		};
	}

	async detect(): Promise<InstanceDetectionReport> {
		const result: InstanceDetectionReport = {
			isAffected: true,
			instanceIssues: [
				{
					title: 'Workflow hooks workflow.activeChange and workflow.activeChangeCurrent deprecated',
					description:
						'The workflow.activeChange and workflow.activeChangeCurrent hooks are deprecated and will be removed. These hooks are being replaced by a new workflow.published hook that provides more consistent behavior and is triggered when any version of a workflow is published.',
					level: 'warning',
				},
			],
			recommendations: [
				{
					action: 'Replace workflow.activeChange with workflow.published',
					description:
						'Update your code to use the new workflow.published hook instead of workflow.activeChange. The new hook will be triggered whenever a workflow version is published.',
				},
				{
					action: 'Replace workflow.activeChangeCurrent with workflow.published',
					description:
						'Update your code to use the new workflow.published hook instead of workflow.activeChangeCurrent. This provides more consistent behavior across workflow publishing actions.',
				},
				{
					action: 'Review custom integrations and extensions',
					description:
						'Check any custom integrations, plugins, or extensions that may be using the deprecated workflow hooks and update them to use workflow.published.',
				},
			],
		};

		return result;
	}
}
