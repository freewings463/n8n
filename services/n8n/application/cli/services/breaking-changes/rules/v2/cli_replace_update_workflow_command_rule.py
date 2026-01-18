"""
MIGRATION-META:
  source_path: packages/cli/src/modules/breaking-changes/rules/v2/cli-replace-update-workflow-command.rule.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/breaking-changes/rules 的工作流模块。导入/依赖:外部:无；内部:@n8n/di；本地:../../types。导出:CliActivateAllWorkflowsRule。关键函数/方法:getMetadata、detect。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/breaking-changes/rules/v2/cli-replace-update-workflow-command.rule.ts -> services/n8n/application/cli/services/breaking-changes/rules/v2/cli_replace_update_workflow_command_rule.py

import { Service } from '@n8n/di';

import type {
	BreakingChangeRuleMetadata,
	IBreakingChangeInstanceRule,
	InstanceDetectionReport,
} from '../../types';
import { BreakingChangeCategory } from '../../types';

@Service()
export class CliActivateAllWorkflowsRule implements IBreakingChangeInstanceRule {
	id: string = 'cli-activate-all-workflows-v2';

	getMetadata(): BreakingChangeRuleMetadata {
		return {
			version: 'v2',
			title: 'CLI command update:workflow replaced',
			description:
				'The CLI command update:workflow has been replaced with publish:workflow and unpublish:workflow for better clarity.',
			category: BreakingChangeCategory.instance,
			severity: 'low',
			documentationUrl:
				'https://docs.n8n.io/2-0-breaking-changes/#replace-cli-command-updateworkflow',
		};
	}

	async detect(): Promise<InstanceDetectionReport> {
		const result: InstanceDetectionReport = {
			isAffected: true,
			instanceIssues: [
				{
					title: 'CLI command update:workflow replaced',
					description:
						'The CLI command update:workflow has been replaced with publish:workflow and unpublish:workflow. If you were using this command in scripts or automation, you will need to update your approach.',
					level: 'info',
				},
			],
			recommendations: [
				{
					action: 'Use the API to activate workflows',
					description:
						'Update automation scripts to use the public API to activate workflows individually instead of the CLI command',
				},
				{
					action: 'Review deployment scripts',
					description:
						'Check any deployment or automation scripts that may have used the CLI command to activate all workflows and update them accordingly',
				},
			],
		};

		return result;
	}
}
