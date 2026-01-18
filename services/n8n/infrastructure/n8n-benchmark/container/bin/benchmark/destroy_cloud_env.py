"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/scripts/destroy-cloud-env.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/scripts 的模块。导入/依赖:外部:zx；内部:无；本地:./clients/terraform-client.mjs。导出:无。关键函数/方法:main、destroyUsingAz、deleteResources、deleteById。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark scripts -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/scripts/destroy-cloud-env.mjs -> services/n8n/infrastructure/n8n-benchmark/container/bin/benchmark/destroy_cloud_env.py

#!/usr/bin/env zx
/**
 * Script that deletes all resources created by the benchmark environment.
 *
 * This scripts tries to delete resources created by Terraform. If Terraform
 * state file is not found, it will try to delete resources using Azure CLI.
 * The terraform state is not persisted, so we want to support both cases.
 */
// @ts-check
import { $, minimist } from 'zx';
import { TerraformClient } from './clients/terraform-client.mjs';

const RESOURCE_GROUP_NAME = 'n8n-benchmarking';

const args = minimist(process.argv.slice(3), {
	boolean: ['debug'],
});

const isVerbose = !!args.debug;

async function main() {
	const terraformClient = new TerraformClient({ isVerbose });

	if (terraformClient.hasTerraformState()) {
		await terraformClient.destroyEnvironment();
	} else {
		await destroyUsingAz();
	}
}

async function destroyUsingAz() {
	const resourcesResult =
		await $`az resource list --resource-group ${RESOURCE_GROUP_NAME} --query "[?tags.Id == 'N8nBenchmark'].{id:id, createdAt:tags.CreatedAt}" -o json`;

	const resources = JSON.parse(resourcesResult.stdout);

	const resourcesToDelete = resources.map((resource) => resource.id);

	if (resourcesToDelete.length === 0) {
		console.log('No resources found in the resource group.');

		return;
	}

	await deleteResources(resourcesToDelete);
}

async function deleteResources(resourceIds) {
	// We don't know the order in which resource should be deleted.
	// Here's a poor person's approach to try deletion until all complete
	const MAX_ITERATIONS = 100;
	let i = 0;
	const toDelete = [...resourceIds];

	console.log(`Deleting ${resourceIds.length} resources...`);
	while (toDelete.length > 0) {
		const resourceId = toDelete.shift();
		const deleted = await deleteById(resourceId);
		if (!deleted) {
			toDelete.push(resourceId);
		}

		if (i++ > MAX_ITERATIONS) {
			console.log(
				`Max iterations reached. Exiting. Could not delete ${toDelete.length} resources.`,
			);
			process.exit(1);
		}
	}
}

async function deleteById(id) {
	try {
		await $`az resource delete --ids ${id}`;
		return true;
	} catch (error) {
		return false;
	}
}

main().catch((error) => {
	console.error('An error occurred destroying cloud env:');
	console.error(error);

	process.exit(1);
});
