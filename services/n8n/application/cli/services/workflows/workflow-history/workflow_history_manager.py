"""
MIGRATION-META:
  source_path: packages/cli/src/workflows/workflow-history/workflow-history-manager.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/workflows/workflow-history 的工作流模块。导入/依赖:外部:luxon；内部:@n8n/constants、@n8n/db、@n8n/di；本地:./workflow-history-helper。导出:WorkflowHistoryManager。关键函数/方法:init、clearInterval、shutdown、prune。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/workflows/workflow-history/workflow-history-manager.ts -> services/n8n/application/cli/services/workflows/workflow-history/workflow_history_manager.py

import { Time } from '@n8n/constants';
import { WorkflowHistoryRepository } from '@n8n/db';
import { Service } from '@n8n/di';
import { DateTime } from 'luxon';

import { getWorkflowHistoryPruneTime } from './workflow-history-helper';

@Service()
export class WorkflowHistoryManager {
	pruneTimer?: NodeJS.Timeout;

	constructor(private workflowHistoryRepo: WorkflowHistoryRepository) {}

	init() {
		if (this.pruneTimer !== undefined) {
			clearInterval(this.pruneTimer);
		}

		this.pruneTimer = setInterval(async () => await this.prune(), 1 * Time.hours.toMilliseconds);
	}

	shutdown() {
		if (this.pruneTimer !== undefined) {
			clearInterval(this.pruneTimer);
			this.pruneTimer = undefined;
		}
	}

	async prune() {
		const pruneHours = getWorkflowHistoryPruneTime();
		// No prune time set (infinite retention)
		if (pruneHours === -1) {
			return;
		}
		const pruneDateTime = DateTime.now().minus({ hours: pruneHours }).toJSDate();

		await this.workflowHistoryRepo.deleteEarlierThanExceptCurrentAndActive(pruneDateTime);
	}
}
