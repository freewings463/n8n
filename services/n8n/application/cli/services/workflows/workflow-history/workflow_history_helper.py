"""
MIGRATION-META:
  source_path: packages/cli/src/workflows/workflow-history/workflow-history-helper.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/workflows/workflow-history 的工作流模块。导入/依赖:外部:无；内部:@n8n/config、@n8n/di、@/license；本地:无。导出:getWorkflowHistoryLicensePruneTime、getWorkflowHistoryPruneTime。关键函数/方法:getWorkflowHistoryLicensePruneTime、getWorkflowHistoryPruneTime。用于承载工作流实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - CLI src/* defaulted to application/services after rule matching
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/workflows/workflow-history/workflow-history-helper.ts -> services/n8n/application/cli/services/workflows/workflow-history/workflow_history_helper.py

import { GlobalConfig } from '@n8n/config';
import { Container } from '@n8n/di';

import { License } from '@/license';

export function getWorkflowHistoryLicensePruneTime() {
	return Container.get(License).getWorkflowHistoryPruneLimit();
}

// Time in hours
export function getWorkflowHistoryPruneTime(): number {
	const licenseTime = Container.get(License).getWorkflowHistoryPruneLimit();
	const configTime = Container.get(GlobalConfig).workflowHistory.pruneTime;

	// License is infinite and config time is infinite
	if (licenseTime === -1) {
		return configTime;
	}

	// License is not infinite but config is, use license time
	if (configTime === -1) {
		return licenseTime;
	}

	// Return the smallest of the license or config if not infinite
	return Math.min(configTime, licenseTime);
}
