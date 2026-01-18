"""
MIGRATION-META:
  source_path: packages/cli/src/modules/breaking-changes/rules/v2/queue-worker-max-stalled-count.rule.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/modules/breaking-changes/rules 的队列模块。导入/依赖:外部:无；内部:@n8n/di；本地:../../types。导出:QueueWorkerMaxStalledCountRule。关键函数/方法:getMetadata、detect。用于承载队列实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/breaking-changes/rules/v2/queue-worker-max-stalled-count.rule.ts -> services/n8n/application/cli/services/breaking-changes/rules/v2/queue_worker_max_stalled_count_rule.py

import { Service } from '@n8n/di';

import type {
	BreakingChangeRuleMetadata,
	IBreakingChangeInstanceRule,
	InstanceDetectionReport,
} from '../../types';
import { BreakingChangeCategory } from '../../types';

@Service()
export class QueueWorkerMaxStalledCountRule implements IBreakingChangeInstanceRule {
	id: string = 'queue-worker-max-stalled-count-v2';

	getMetadata(): BreakingChangeRuleMetadata {
		return {
			version: 'v2',
			title: 'Remove QUEUE_WORKER_MAX_STALLED_COUNT',
			description:
				'The QUEUE_WORKER_MAX_STALLED_COUNT environment variable has been removed and will be ignored',
			category: BreakingChangeCategory.environment,
			severity: 'low',
			documentationUrl:
				'https://docs.n8n.io/2-0-breaking-changes/#remove-queue_worker_max_stalled_count',
		};
	}

	async detect(): Promise<InstanceDetectionReport> {
		const result: InstanceDetectionReport = {
			isAffected: false,
			instanceIssues: [],
			recommendations: [],
		};

		// If QUEUE_WORKER_MAX_STALLED_COUNT is not set, the instance is not affected
		// because the default behavior remains unchanged
		if (!process.env.QUEUE_WORKER_MAX_STALLED_COUNT) {
			return result;
		}

		result.isAffected = true;
		result.instanceIssues.push({
			title: 'QUEUE_WORKER_MAX_STALLED_COUNT is deprecated',
			description:
				'The QUEUE_WORKER_MAX_STALLED_COUNT environment variable has been removed. Any customization will be ignored in v2.',
			level: 'warning',
		});

		result.recommendations.push({
			action: 'Remove environment variable',
			description:
				'Remove QUEUE_WORKER_MAX_STALLED_COUNT from your environment configuration as it no longer has any effect',
		});

		return result;
	}
}
