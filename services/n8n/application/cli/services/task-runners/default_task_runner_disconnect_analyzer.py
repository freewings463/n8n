"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/default-task-runner-disconnect-analyzer.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/task-runners 的模块。导入/依赖:外部:无；内部:@n8n/config、@n8n/di；本地:./errors/task-runner-disconnected-error、./errors/task-runner-failed-heartbeat.error。导出:DefaultTaskRunnerDisconnectAnalyzer。关键函数/方法:toDisconnectError。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/default-task-runner-disconnect-analyzer.ts -> services/n8n/application/cli/services/task-runners/default_task_runner_disconnect_analyzer.py

import { GlobalConfig } from '@n8n/config';
import { Container, Service } from '@n8n/di';

import type {
	DisconnectAnalyzer,
	DisconnectErrorOptions,
} from '@/task-runners/task-broker/task-broker-types';

import { TaskRunnerDisconnectedError } from './errors/task-runner-disconnected-error';
import { TaskRunnerFailedHeartbeatError } from './errors/task-runner-failed-heartbeat.error';

/**
 * Analyzes the disconnect reason of a task runner to provide a more
 * meaningful error message to the user.
 */
@Service()
export class DefaultTaskRunnerDisconnectAnalyzer implements DisconnectAnalyzer {
	get isCloudDeployment() {
		return Container.get(GlobalConfig).deployment.type === 'cloud';
	}

	async toDisconnectError(opts: DisconnectErrorOptions): Promise<Error> {
		const { reason, heartbeatInterval } = opts;

		if (reason === 'failed-heartbeat-check' && heartbeatInterval) {
			return new TaskRunnerFailedHeartbeatError(
				heartbeatInterval,
				Container.get(GlobalConfig).deployment.type !== 'cloud',
			);
		}

		return new TaskRunnerDisconnectedError(
			opts.runnerId ?? 'Unknown runner ID',
			this.isCloudDeployment,
		);
	}
}
