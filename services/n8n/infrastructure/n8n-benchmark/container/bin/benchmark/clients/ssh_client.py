"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/scripts/clients/ssh-client.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/scripts/clients 的模块。导入/依赖:外部:zx；内部:无；本地:无。导出:SshClient。关键函数/方法:ssh、scp。用于承载该模块实现细节，并通过导出对外提供能力。注释目标:@ts-check。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark scripts -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/scripts/clients/ssh-client.mjs -> services/n8n/infrastructure/n8n-benchmark/container/bin/benchmark/clients/ssh_client.py

// @ts-check
import { $ } from 'zx';

export class SshClient {
	/**
	 *
	 * @param {{ privateKeyPath: string; ip: string; username: string; verbose?: boolean }} param0
	 */
	constructor({ privateKeyPath, ip, username, verbose = false }) {
		this.verbose = verbose;
		this.privateKeyPath = privateKeyPath;
		this.ip = ip;
		this.username = username;

		this.$$ = $({
			verbose,
		});
	}

	/**
	 * @param {string} command
	 * @param {{ verbose?: boolean }} [options]
	 */
	async ssh(command, options = {}) {
		const $$ = options?.verbose ? $({ verbose: true }) : this.$$;

		const target = `${this.username}@${this.ip}`;

		await $$`ssh -i ${this.privateKeyPath} -o StrictHostKeyChecking=accept-new ${target} ${command}`;
	}

	async scp(source, destination) {
		const target = `${this.username}@${this.ip}:${destination}`;
		await this
			.$$`scp -i ${this.privateKeyPath} -o StrictHostKeyChecking=accept-new ${source} ${target}`;
	}
}
