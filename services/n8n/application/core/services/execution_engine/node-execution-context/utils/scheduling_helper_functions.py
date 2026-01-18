"""
MIGRATION-META:
  source_path: packages/core/src/execution-engine/node-execution-context/utils/scheduling-helper-functions.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/core/src/execution-engine/node-execution-context/utils 的执行工具。导入/依赖:外部:无；内部:@n8n/di、n8n-workflow；本地:../../scheduled-task-manager。导出:getSchedulingFunctions。关键函数/方法:getSchedulingFunctions。用于提供执行通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Core execution engine -> application/services/execution_engine
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/execution-engine/node-execution-context/utils/scheduling-helper-functions.ts -> services/n8n/application/core/services/execution_engine/node-execution-context/utils/scheduling_helper_functions.py

import { Container } from '@n8n/di';
import type { SchedulingFunctions, Workflow, CronContext, Cron } from 'n8n-workflow';

import { ScheduledTaskManager } from '../../scheduled-task-manager';

export const getSchedulingFunctions = (
	workflowId: Workflow['id'],
	timezone: Workflow['timezone'],
	nodeId: string,
): SchedulingFunctions => {
	const scheduledTaskManager = Container.get(ScheduledTaskManager);
	return {
		registerCron: ({ expression, recurrence }: Cron, onTick) => {
			const ctx: CronContext = {
				expression,
				recurrence,
				nodeId,
				workflowId,
				timezone,
			};

			return scheduledTaskManager.registerCron(ctx, onTick);
		},
	};
};
