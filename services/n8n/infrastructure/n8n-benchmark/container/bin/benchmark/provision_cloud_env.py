"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/scripts/provision-cloud-env.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/scripts 的模块。导入/依赖:外部:zx；内部:无；本地:./clients/terraform-client.mjs。导出:无。关键函数/方法:provision、ensureDependencies。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark scripts -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/scripts/provision-cloud-env.mjs -> services/n8n/infrastructure/n8n-benchmark/container/bin/benchmark/provision_cloud_env.py

#!/usr/bin/env zx
/**
 * Provisions the cloud benchmark environment
 *
 * NOTE: Must be run in the root of the package.
 */
// @ts-check
import { which, minimist } from 'zx';
import { TerraformClient } from './clients/terraform-client.mjs';

const args = minimist(process.argv.slice(3), {
	boolean: ['debug'],
});

const isVerbose = !!args.debug;

export async function provision() {
	await ensureDependencies();

	const terraformClient = new TerraformClient({
		isVerbose,
	});

	await terraformClient.provisionEnvironment();
}

async function ensureDependencies() {
	await which('terraform');
}

provision().catch((error) => {
	console.error('An error occurred while provisioning cloud env:');
	console.error(error);

	process.exit(1);
});
