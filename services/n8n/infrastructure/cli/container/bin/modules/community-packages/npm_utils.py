"""
MIGRATION-META:
  source_path: packages/cli/src/modules/community-packages/npm-utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/modules/community-packages 的模块。导入/依赖:外部:axios、node:child_process、node:util；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:isDnsError、isNpmError、sanitizeRegistryUrl、verifyIntegrity、checkIfVersionExistsOrThrow。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected child_process execution -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/modules/community-packages/npm-utils.ts -> services/n8n/infrastructure/cli/container/bin/modules/community-packages/npm_utils.py

import axios from 'axios';
import { jsonParse, UnexpectedError } from 'n8n-workflow';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const asyncExecFile = promisify(execFile);

const REQUEST_TIMEOUT = 30000;

function isDnsError(error: unknown): boolean {
	const message = error instanceof Error ? error.message : String(error);
	return message.includes('getaddrinfo') || message.includes('ENOTFOUND');
}

function isNpmError(error: unknown): boolean {
	const message = error instanceof Error ? error.message : String(error);
	return (
		message.includes('npm ERR!') ||
		message.includes('E404') ||
		message.includes('404 Not Found') ||
		message.includes('ENOTFOUND')
	);
}

function sanitizeRegistryUrl(registryUrl: string): string {
	return registryUrl.replace(/\/+$/, '');
}

export async function verifyIntegrity(
	packageName: string,
	version: string,
	registryUrl: string,
	expectedIntegrity: string,
) {
	const url = `${sanitizeRegistryUrl(registryUrl)}/${encodeURIComponent(packageName)}`;

	try {
		const metadata = await axios.get<{ dist: { integrity?: string } }>(`${url}/${version}`, {
			timeout: REQUEST_TIMEOUT,
		});

		const integrity = metadata?.data?.dist?.integrity;
		if (integrity !== expectedIntegrity) {
			throw new UnexpectedError('Checksum verification failed. Package integrity does not match.');
		}
		return;
	} catch (error) {
		try {
			const { stdout } = await asyncExecFile('npm', [
				'view',
				`${packageName}@${version}`,
				'dist.integrity',
				`--registry=${sanitizeRegistryUrl(registryUrl)}`,
				'--json',
			]);

			const integrity = jsonParse(stdout);
			if (integrity !== expectedIntegrity) {
				throw new UnexpectedError(
					'Checksum verification failed. Package integrity does not match.',
				);
			}
			return;
		} catch (cliError) {
			if (isDnsError(cliError) || isNpmError(cliError)) {
				throw new UnexpectedError(
					'Checksum verification failed. Please check your network connection and try again.',
				);
			}
			throw new UnexpectedError('Checksum verification failed');
		}
	}
}

export async function checkIfVersionExistsOrThrow(
	packageName: string,
	version: string,
	registryUrl: string,
): Promise<true> {
	const url = `${sanitizeRegistryUrl(registryUrl)}/${encodeURIComponent(packageName)}`;

	try {
		await axios.get(`${url}/${version}`, { timeout: REQUEST_TIMEOUT });
		return true;
	} catch (error) {
		try {
			const { stdout } = await asyncExecFile('npm', [
				'view',
				`${packageName}@${version}`,
				'version',
				`--registry=${sanitizeRegistryUrl(registryUrl)}`,
				'--json',
			]);

			const versionInfo = jsonParse(stdout);
			if (versionInfo === version) {
				return true;
			}

			throw new UnexpectedError('Failed to check package version existence');
		} catch (cliError) {
			const message = cliError instanceof Error ? cliError.message : String(cliError);

			if (message.includes('E404') || message.includes('404 Not Found')) {
				throw new UnexpectedError('Package version does not exist');
			}

			if (isDnsError(cliError) || isNpmError(cliError)) {
				throw new UnexpectedError(
					'The community nodes service is temporarily unreachable. Please try again later.',
				);
			}

			throw new UnexpectedError('Failed to check package version existence');
		}
	}
}
