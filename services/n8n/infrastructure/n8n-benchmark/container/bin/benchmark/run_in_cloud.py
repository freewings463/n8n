"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/scripts/run-in-cloud.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/scripts 的模块。导入/依赖:外部:zx；内部:无；本地:./clients/ssh-client.mjs、./clients/terraform-client.mjs、./utils/flags.mjs。导出:无。关键函数/方法:runInCloud、ensureDependencies、runBenchmarksOnVm、runBenchmarkForN8nSetup、ensureVmIsReachable、transferScriptsToVm。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark scripts -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/scripts/run-in-cloud.mjs -> services/n8n/infrastructure/n8n-benchmark/container/bin/benchmark/run_in_cloud.py

#!/usr/bin/env zx
/**
 * Script to run benchmarks on the cloud benchmark environment.
 * This script will:
 * 	1. Provision a benchmark environment using Terraform.
 * 	2. Run the benchmarks on the VM.
 * 	3. Destroy the cloud environment.
 *
 * NOTE: Must be run in the root of the package.
 */
// @ts-check
import { sleep, which, $, tmpdir } from 'zx';
import path from 'path';
import { SshClient } from './clients/ssh-client.mjs';
import { TerraformClient } from './clients/terraform-client.mjs';
import { flagsObjectToCliArgs } from './utils/flags.mjs';

/**
 * @typedef {Object} BenchmarkEnv
 * @property {string} vmName
 * @property {string} ip
 * @property {string} sshUsername
 * @property {string} sshPrivateKeyPath
 */

/**
 * @typedef {Object} Config
 * @property {boolean} isVerbose
 * @property {string[]} n8nSetupsToUse
 * @property {string} n8nTag
 * @property {string} benchmarkTag
 * @property {string} [k6ApiToken]
 * @property {string} [resultWebhookUrl]
 * @property {string} [resultWebhookAuthHeader]
 * @property {string} [n8nLicenseCert]
 * @property {string} [vus]
 * @property {string} [duration]
 * @property {string} [scenarioFilter]
 *
 * @param {Config} config
 */
export async function runInCloud(config) {
	await ensureDependencies();

	const terraformClient = new TerraformClient({
		isVerbose: config.isVerbose,
	});

	const benchmarkEnv = await terraformClient.getTerraformOutputs();

	await runBenchmarksOnVm(config, benchmarkEnv);
}

async function ensureDependencies() {
	await which('terraform');
	await which('az');
}

/**
 * @param {Config} config
 * @param {BenchmarkEnv} benchmarkEnv
 */
async function runBenchmarksOnVm(config, benchmarkEnv) {
	console.log(`Setting up the environment...`);

	const sshClient = new SshClient({
		ip: benchmarkEnv.ip,
		username: benchmarkEnv.sshUsername,
		privateKeyPath: benchmarkEnv.sshPrivateKeyPath,
		verbose: config.isVerbose,
	});

	await ensureVmIsReachable(sshClient);

	const scriptsDir = await transferScriptsToVm(sshClient, config);

	// Bootstrap the environment with dependencies
	console.log('Running bootstrap script...');
	const bootstrapScriptPath = path.join(scriptsDir, 'bootstrap.sh');
	await sshClient.ssh(`chmod a+x ${bootstrapScriptPath} && ${bootstrapScriptPath}`);

	// Give some time for the VM to be ready
	await sleep(1000);

	const failures = [];

	for (const n8nSetup of config.n8nSetupsToUse) {
		try {
			await runBenchmarkForN8nSetup({
				config,
				sshClient,
				scriptsDir,
				n8nSetup,
			});
		} catch (error) {
			console.error(`Benchmark failed for ${n8nSetup}:`, error.message);
			failures.push(n8nSetup);
		}
	}

	if (failures.length > 0) {
		throw new Error(`Benchmarks failed for setups: ${failures.join(', ')}`);
	}
}

/**
 * @param {{ config: Config; sshClient: any; scriptsDir: string; n8nSetup: string; }} opts
 */
async function runBenchmarkForN8nSetup({ config, sshClient, scriptsDir, n8nSetup }) {
	console.log(`Running benchmarks for ${n8nSetup}...`);
	const runScriptPath = path.join(scriptsDir, 'run-for-n8n-setup.mjs');

	const cliArgs = flagsObjectToCliArgs({
		n8nDockerTag: config.n8nTag,
		benchmarkDockerTag: config.benchmarkTag,
		k6ApiToken: config.k6ApiToken,
		resultWebhookUrl: config.resultWebhookUrl,
		resultWebhookAuthHeader: config.resultWebhookAuthHeader,
		n8nLicenseCert: config.n8nLicenseCert,
		scenarioFilter: config.scenarioFilter,
		vus: config.vus,
		duration: config.duration,
		env: 'cloud',
	});

	const flagsString = cliArgs.join(' ');

	await sshClient.ssh(`npx zx ${runScriptPath} ${flagsString} ${n8nSetup}`, {
		// Test run should always log its output
		verbose: true,
	});
}

async function ensureVmIsReachable(sshClient) {
	try {
		await sshClient.ssh('echo "VM is reachable"');
	} catch (error) {
		console.error(`VM is not reachable: ${error.message}`);
		console.error(
			`Did you provision the cloud environment first with 'pnpm provision-cloud-env'? You can also run the benchmarks locally with 'pnpm run benchmark-locally'.`,
		);
		process.exit(1);
	}
}

/**
 * @returns Path where the scripts are located on the VM
 */
async function transferScriptsToVm(sshClient, config) {
	const cwd = process.cwd();
	const scriptsDir = path.resolve(cwd, './scripts');
	const tarFilename = 'scripts.tar.gz';
	const scriptsTarPath = path.join(tmpdir('n8n-benchmark'), tarFilename);

	const $$ = $({ verbose: config.isVerbose });

	// Compress the scripts folder
	await $$`tar -czf ${scriptsTarPath} ${scriptsDir} -C ${cwd} ./scripts`;

	// Transfer the scripts to the VM
	await sshClient.scp(scriptsTarPath, `~/${tarFilename}`);

	// Extract the scripts on the VM
	await sshClient.ssh(`tar -xzf ~/${tarFilename}`);

	return '~/scripts';
}
