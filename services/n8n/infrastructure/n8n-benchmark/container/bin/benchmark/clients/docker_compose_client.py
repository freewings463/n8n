"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/scripts/clients/docker-compose-client.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/scripts/clients 的模块。导入/依赖:外部:zx；内部:无；本地:无。导出:DockerComposeClient。关键函数/方法:$、resolveExecutableIfNeeded。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark scripts -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/scripts/clients/docker-compose-client.mjs -> services/n8n/infrastructure/n8n-benchmark/container/bin/benchmark/clients/docker_compose_client.py

import { which } from 'zx';

export class DockerComposeClient {
	/**
	 *
	 * @param {{ $: Shell; verbose?: boolean }} opts
	 */
	constructor({ $ }) {
		this.$$ = $;
	}

	async $(...args) {
		await this.resolveExecutableIfNeeded();

		if (this.isCompose) {
			return await this.$$`docker-compose ${args}`;
		} else {
			return await this.$$`docker compose ${args}`;
		}
	}

	async resolveExecutableIfNeeded() {
		if (this.isResolved) {
			return;
		}

		// The VM deployment doesn't have `docker compose` available,
		// so try to resolve the `docker-compose` first
		const compose = await which('docker-compose', { nothrow: true });
		if (compose) {
			this.isResolved = true;
			this.isCompose = true;
			return;
		}

		const docker = await which('docker', { nothrow: true });
		if (docker) {
			this.isResolved = true;
			this.isCompose = false;
			return;
		}

		throw new Error('Could not resolve docker-compose or docker');
	}
}
