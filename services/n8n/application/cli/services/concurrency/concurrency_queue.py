"""
MIGRATION-META:
  source_path: packages/cli/src/concurrency/concurrency-queue.ts
  target_context: n8n
  target_layer: Application
  responsibility: 位于 packages/cli/src/concurrency 的队列模块。导入/依赖:外部:无；内部:@n8n/di、@/typed-emitter；本地:无。导出:ConcurrencyQueue。关键函数/方法:enqueue、dequeue、remove、getAll、has、resolveNext、resolve。用于承载队列实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected @Service from @n8n/di
    - Rewrite implementation for Application layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/concurrency/concurrency-queue.ts -> services/n8n/application/cli/services/concurrency/concurrency_queue.py

import { Service } from '@n8n/di';

import { TypedEmitter } from '@/typed-emitter';

type ConcurrencyEvents = {
	'execution-throttled': { executionId: string };
	'execution-released': string;
	'concurrency-check': { capacity: number };
};

@Service()
export class ConcurrencyQueue extends TypedEmitter<ConcurrencyEvents> {
	private readonly queue: Array<{
		executionId: string;
		resolve: () => void;
	}> = [];

	constructor(private capacity: number) {
		super();
	}

	async enqueue(executionId: string) {
		this.capacity--;

		this.debouncedEmit('concurrency-check', { capacity: this.capacity });

		if (this.capacity < 0) {
			this.emit('execution-throttled', { executionId });

			// eslint-disable-next-line @typescript-eslint/return-await
			return new Promise<void>((resolve) => this.queue.push({ executionId, resolve }));
		}
	}

	get currentCapacity() {
		return this.capacity;
	}

	dequeue() {
		this.capacity++;

		this.resolveNext();
	}

	remove(executionId: string) {
		const index = this.queue.findIndex((item) => item.executionId === executionId);

		if (index > -1) {
			this.queue.splice(index, 1);

			this.capacity++;

			this.resolveNext();
		}
	}

	getAll() {
		return new Set(this.queue.map((item) => item.executionId));
	}

	has(executionId: string) {
		return this.queue.some((item) => item.executionId === executionId);
	}

	private resolveNext() {
		const item = this.queue.shift();

		if (!item) return;

		const { resolve, executionId } = item;

		this.emit('execution-released', executionId);

		resolve();
	}
}
