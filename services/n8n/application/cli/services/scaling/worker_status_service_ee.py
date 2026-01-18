"""
MIGRATION-META:
  source_path: packages/cli/src/scaling/worker-status.service.ee.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/scaling 的服务。导入/依赖:外部:node:process；内部:@n8n/api-types、@n8n/decorators、@n8n/di、n8n-core、@/constants、@/push；本地:./job-processor、./pubsub/publisher.service。导出:WorkerStatusService。关键函数/方法:requestWorkerStatus、handleWorkerStatusResponse、publishWorkerResponse、generateStatus、getOsCpuString。用于封装该模块业务流程，对上提供稳定调用面。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/scaling/worker-status.service.ee.ts -> services/n8n/application/cli/services/scaling/worker_status_service_ee.py

import { WorkerStatus } from '@n8n/api-types';
import { OnPubSubEvent } from '@n8n/decorators';
import { Service } from '@n8n/di';
import { InstanceSettings } from 'n8n-core';
import os from 'node:os';
import process from 'node:process';

import { N8N_VERSION } from '@/constants';
import { Push } from '@/push';

import { JobProcessor } from './job-processor';
import { Publisher } from './pubsub/publisher.service';

@Service()
export class WorkerStatusService {
	constructor(
		private readonly jobProcessor: JobProcessor,
		private readonly instanceSettings: InstanceSettings,
		private readonly publisher: Publisher,
		private readonly push: Push,
	) {}

	async requestWorkerStatus() {
		if (this.instanceSettings.instanceType !== 'main') return;

		return await this.publisher.publishCommand({ command: 'get-worker-status' });
	}

	@OnPubSubEvent('response-to-get-worker-status', { instanceType: 'main' })
	handleWorkerStatusResponse(payload: WorkerStatus) {
		this.push.broadcast({
			type: 'sendWorkerStatusMessage',
			data: {
				workerId: payload.senderId,
				status: payload,
			},
		});
	}

	@OnPubSubEvent('get-worker-status', { instanceType: 'worker' })
	async publishWorkerResponse() {
		await this.publisher.publishWorkerResponse({
			senderId: this.instanceSettings.hostId,
			response: 'response-to-get-worker-status',
			payload: this.generateStatus(),
		});
	}

	private generateStatus(): WorkerStatus {
		const constrainedMemory = process.constrainedMemory();

		// See https://github.com/nodejs/node/issues/59227 for information about why we cap at MAX_SAFE_INTEGER
		// The number 18446744073709552000 does come back when running in a container with no constraints
		const isInContainer = constrainedMemory > 0 && constrainedMemory < Number.MAX_SAFE_INTEGER;
		return {
			senderId: this.instanceSettings.hostId,
			runningJobsSummary: this.jobProcessor.getRunningJobsSummary(),
			isInContainer,
			process: {
				memory: {
					available: process.availableMemory(),
					constraint: process.constrainedMemory(),
					...process.memoryUsage(),
				},
				uptime: process.uptime(),
			},
			host: {
				memory: {
					total: os.totalmem(),
					free: os.freemem(),
				},
			},
			freeMem: os.freemem(),
			totalMem: os.totalmem(),
			uptime: process.uptime(),
			loadAvg: os.loadavg(),
			cpus: this.getOsCpuString(),
			arch: os.arch(),
			platform: os.platform(),
			hostname: os.hostname(),
			interfaces: Object.values(os.networkInterfaces()).flatMap((interfaces) =>
				(interfaces ?? [])?.map((net) => ({
					family: net.family,
					address: net.address,
					internal: net.internal,
				})),
			),
			version: N8N_VERSION,
		};
	}

	private getOsCpuString() {
		const cpus = os.cpus();

		if (cpus.length === 0) return 'no CPU info';

		return `${cpus.length}x ${cpus[0].model}`;
	}
}
