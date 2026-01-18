"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/task-managers/local-task-requester.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/task-runners/task-managers 的模块。导入/依赖:外部:无；内部:@n8n/config、@n8n/di、@n8n/task-runner、n8n-core、@/events/event.service、@/node-types 等1项；本地:./task-requester。导出:LocalTaskRequester。关键函数/方法:registerRequester、sendMessage。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/task-managers/local-task-requester.ts -> services/n8n/application/cli/services/task-runners/task-managers/local_task_requester.py

import { GlobalConfig, TaskRunnersConfig } from '@n8n/config';
import { Container, Service } from '@n8n/di';
import type { RequesterMessage } from '@n8n/task-runner';
import { ErrorReporter } from 'n8n-core';

import { EventService } from '@/events/event.service';
import { NodeTypes } from '@/node-types';
import type { RequesterMessageCallback } from '@/task-runners/task-broker/task-broker.service';
import { TaskBroker } from '@/task-runners/task-broker/task-broker.service';

import { TaskRequester } from './task-requester';

@Service()
export class LocalTaskRequester extends TaskRequester {
	taskBroker: TaskBroker;

	id = 'local-task-requester';

	constructor(
		nodeTypes: NodeTypes,
		eventService: EventService,
		taskRunnersConfig: TaskRunnersConfig,
		globalConfig: GlobalConfig,
		errorReporter: ErrorReporter,
	) {
		super(nodeTypes, eventService, taskRunnersConfig, globalConfig, errorReporter);
		this.registerRequester();
	}

	registerRequester() {
		this.taskBroker = Container.get(TaskBroker);

		this.taskBroker.registerRequester(
			this.id,
			this.onMessage.bind(this) as RequesterMessageCallback,
		);
	}

	sendMessage(message: RequesterMessage.ToBroker.All) {
		void this.taskBroker.onRequesterMessage(this.id, message);
	}
}
