"""
MIGRATION-META:
  source_path: packages/cli/src/commands/ttwf/worker-pool.ts
  target_context: n8n
  target_layer: Interface
  responsibility: 位于 packages/cli/src/commands/ttwf 的模块。导入/依赖:外部:无；内部:无；本地:无。导出:WorkerPool。关键函数/方法:execute、resolve、reject、processQueue。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - CLI command -> presentation/cli/commands
    - Rewrite implementation for Interface layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/commands/ttwf/worker-pool.ts -> services/n8n/presentation/cli/cli/commands/ttwf/worker_pool.py

export class WorkerPool<T> {
	private queue: Array<() => Promise<T>> = [];

	private activeWorkers = 0;

	constructor(private maxWorkers: number) {}

	async execute(task: () => Promise<T>): Promise<T> {
		// If under limit, execute immediately
		if (this.activeWorkers < this.maxWorkers) {
			this.activeWorkers++;
			try {
				const result = await task();
				this.activeWorkers--;
				this.processQueue();

				return result;
			} catch (error) {
				this.activeWorkers--;
				this.processQueue();

				throw error;
			}
		}

		// Otherwise queue the task
		return await new Promise((resolve, reject) => {
			this.queue.push(async () => {
				try {
					const result = await task();
					resolve(result);
					return result;
				} catch (error) {
					reject(error);
					throw error;
				}
			});
		});
	}

	private processQueue() {
		if (this.queue.length > 0 && this.activeWorkers < this.maxWorkers) {
			const task = this.queue.shift()!;
			void this.execute(task);
		}
	}
}
