"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/scripts/clients/terraform-client.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/scripts/clients 的模块。导入/依赖:外部:zx；内部:无；本地:无。导出:TerraformClient。关键函数/方法:provisionEnvironment、getTerraformOutputs、hasTerraformState、destroyEnvironment、getTerraformOutput、extractPrivateKey。用于承载该模块实现细节，并通过导出对外提供能力。注释目标:@ts-check。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark scripts -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/scripts/clients/terraform-client.mjs -> services/n8n/infrastructure/n8n-benchmark/container/bin/benchmark/clients/terraform_client.py

// @ts-check

import path from 'path';
import { $, fs } from 'zx';

const paths = {
	infraCodeDir: path.resolve('infra'),
	terraformStateFile: path.join(path.resolve('infra'), 'terraform.tfstate'),
};

export class TerraformClient {
	constructor({ isVerbose = false }) {
		this.isVerbose = isVerbose;
		this.$$ = $({
			cwd: paths.infraCodeDir,
			verbose: isVerbose,
		});
	}

	/**
	 * Provisions the environment
	 */
	async provisionEnvironment() {
		console.log('Provisioning cloud environment...');

		await this.$$`terraform init`;
		await this.$$`terraform apply -input=false -auto-approve`;
	}

	/**
	 * @typedef {Object} BenchmarkEnv
	 * @property {string} vmName
	 * @property {string} ip
	 * @property {string} sshUsername
	 * @property {string} sshPrivateKeyPath
	 *
	 * @returns {Promise<BenchmarkEnv>}
	 */
	async getTerraformOutputs() {
		const privateKeyName = await this.extractPrivateKey();

		return {
			ip: await this.getTerraformOutput('ip'),
			sshUsername: await this.getTerraformOutput('ssh_username'),
			sshPrivateKeyPath: path.join(paths.infraCodeDir, privateKeyName),
			vmName: await this.getTerraformOutput('vm_name'),
		};
	}

	hasTerraformState() {
		return fs.existsSync(paths.terraformStateFile);
	}

	async destroyEnvironment() {
		console.log('Destroying cloud environment...');

		await this.$$`terraform destroy -input=false -auto-approve`;
	}

	async getTerraformOutput(key) {
		const output = await this.$$`terraform output -raw ${key}`;
		return output.stdout.trim();
	}

	async extractPrivateKey() {
		await this.$$`terraform output -raw ssh_private_key > privatekey.pem`;
		await this.$$`chmod 600 privatekey.pem`;

		return 'privatekey.pem';
	}
}
