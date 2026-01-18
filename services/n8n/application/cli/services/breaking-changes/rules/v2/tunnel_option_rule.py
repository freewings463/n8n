"""
MIGRATION-META:
  source_path: packages/cli/src/modules/breaking-changes/rules/v2/tunnel-option.rule.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/breaking-changes/rules 的模块。导入/依赖:外部:无；内部:@n8n/di；本地:../../types。导出:TunnelOptionRule。关键函数/方法:getMetadata、detect。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/breaking-changes/rules/v2/tunnel-option.rule.ts -> services/n8n/application/cli/services/breaking-changes/rules/v2/tunnel_option_rule.py

import { Service } from '@n8n/di';

import type {
	BreakingChangeRuleMetadata,
	IBreakingChangeInstanceRule,
	InstanceDetectionReport,
} from '../../types';
import { BreakingChangeCategory } from '../../types';

@Service()
export class TunnelOptionRule implements IBreakingChangeInstanceRule {
	id: string = 'tunnel-option-v2';

	getMetadata(): BreakingChangeRuleMetadata {
		return {
			version: 'v2',
			title: 'Remove n8n --tunnel option',
			description: 'The --tunnel CLI option has been removed and will be ignored',
			category: BreakingChangeCategory.instance,
			severity: 'low',
			documentationUrl: 'https://docs.n8n.io/2-0-breaking-changes/#remove-n8n-tunnel-option',
		};
	}

	async detect(): Promise<InstanceDetectionReport> {
		const result: InstanceDetectionReport = {
			isAffected: true,
			instanceIssues: [
				{
					title: '--tunnel option removed',
					description:
						'The --tunnel CLI option is no longer available. If you were using this feature, calls with the --tunnel flag will ignore the flag and not run the tunnel system.',
					level: 'info',
				},
			],
			recommendations: [],
		};

		return result;
	}
}
