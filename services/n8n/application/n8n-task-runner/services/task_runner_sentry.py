"""
MIGRATION-META:
  source_path: packages/@n8n/task-runner/src/task-runner-sentry.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/@n8n/task-runner/src 的模块。导入/依赖:外部:@sentry/core；内部:@n8n/di、n8n-core；本地:./config/sentry-config。导出:TaskRunnerSentry。关键函数/方法:initIfEnabled、shutdown、isUserCodeError。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/task-runner/src/task-runner-sentry.ts -> services/n8n/application/n8n-task-runner/services/task_runner_sentry.py

import { Service } from '@n8n/di';
import type { ErrorEvent, Exception } from '@sentry/core';
import { ErrorReporter } from 'n8n-core';

import { SentryConfig } from './config/sentry-config';

/**
 * Sentry service for the task runner.
 */
@Service()
export class TaskRunnerSentry {
	constructor(
		private readonly config: SentryConfig,
		private readonly errorReporter: ErrorReporter,
	) {}

	async initIfEnabled() {
		const { dsn, n8nVersion, environment, deploymentName } = this.config;

		if (!dsn) return;

		await this.errorReporter.init({
			serverType: 'task_runner',
			dsn,
			release: `n8n@${n8nVersion}`,
			environment,
			serverName: deploymentName,
			beforeSendFilter: this.filterOutUserCodeErrors,
			withEventLoopBlockDetection: false,
		});
	}

	async shutdown() {
		if (!this.config.dsn) return;

		await this.errorReporter.shutdown();
	}

	/**
	 * Filter out errors originating from user provided code.
	 * It is possible for users to create code that causes unhandledrejections
	 * that end up in the sentry error reporting.
	 */
	filterOutUserCodeErrors = (event: ErrorEvent) => {
		const error = event?.exception?.values?.[0];

		return error ? this.isUserCodeError(error) : false;
	};

	/**
	 * Check if the error is originating from user provided code.
	 * It is possible for users to create code that causes unhandledrejections
	 * that end up in the sentry error reporting.
	 */
	private isUserCodeError(error: Exception) {
		const frames = error.stacktrace?.frames;
		if (!frames) return false;

		return frames.some((frame) => {
			if (frame.filename === 'node:vm' && frame.function === 'runInContext') {
				return true;
			}

			if (frame.filename === 'evalmachine.<anonymous>') {
				return true;
			}

			if (frame.function === 'VmCodeWrapper') {
				return true;
			}

			return false;
		});
	}
}
