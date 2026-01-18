"""
MIGRATION-META:
  source_path: packages/testing/containers/services/task-runner.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/testing/containers/services 的服务。导入/依赖:外部:testcontainers；内部:无；本地:../helpers/utils、../test-containers、./types。导出:TaskRunnerConfig、TaskRunnerMeta、TaskRunnerResult、taskRunner。关键函数/方法:start、getOptions。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Testing package (containers harness) -> tests/fixtures/containers
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/testing/containers/services/task-runner.ts -> services/n8n/tests/testing/fixtures/containers/services/task_runner.py

import { GenericContainer, Wait } from 'testcontainers';

import { createSilentLogConsumer } from '../helpers/utils';
import { TEST_CONTAINER_IMAGES } from '../test-containers';
import type { Service, ServiceResult } from './types';

export interface TaskRunnerConfig {
	taskBrokerUri: string;
}

export interface TaskRunnerMeta {
	taskBrokerUri: string;
}

export type TaskRunnerResult = ServiceResult<TaskRunnerMeta>;

export const taskRunner: Service<TaskRunnerResult> = {
	description: 'Task Runner',
	shouldStart: () => true,

	getOptions(ctx) {
		const { workers, mains, projectName } = ctx;
		const taskBrokerHost =
			workers > 0
				? `${projectName}-n8n-worker-1`
				: mains > 1
					? `${projectName}-n8n-main-1`
					: `${projectName}-n8n`;
		return { taskBrokerUri: `http://${taskBrokerHost}:5679` } as TaskRunnerConfig;
	},

	async start(network, projectName, config?: unknown): Promise<TaskRunnerResult> {
		const { taskBrokerUri } = config as TaskRunnerConfig;
		const { consumer, throwWithLogs } = createSilentLogConsumer();

		try {
			const container = await new GenericContainer(TEST_CONTAINER_IMAGES.taskRunner)
				.withNetwork(network)
				.withNetworkAliases(`${projectName}-task-runner`)
				.withExposedPorts(5680)
				.withEnvironment({
					N8N_RUNNERS_AUTH_TOKEN: 'test',
					N8N_RUNNERS_LAUNCHER_LOG_LEVEL: 'debug',
					N8N_RUNNERS_TASK_BROKER_URI: taskBrokerUri,
					N8N_RUNNERS_MAX_CONCURRENCY: '5',
					N8N_RUNNERS_AUTO_SHUTDOWN_TIMEOUT: '0', // Disabled in tests to prevent cold-start delays
				})
				.withWaitStrategy(Wait.forListeningPorts())
				.withLabels({
					'com.docker.compose.project': projectName,
					'com.docker.compose.service': 'task-runner',
				})
				.withName(`${projectName}-task-runner`)
				.withReuse()
				.withLogConsumer(consumer)
				.start();

			return {
				container,
				meta: {
					taskBrokerUri,
				},
			};
		} catch (error) {
			return throwWithLogs(error);
		}
	},
};
