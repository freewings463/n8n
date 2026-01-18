"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/utils/package-manager.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/utils 的工具。导入/依赖:外部:node:fs/promises；内部:无；本地:无。导出:detectPackageManagerFromUserAgent。关键函数/方法:detectPackageManagerFromUserAgent、detectPackageManagerFromLockFiles、detectPackageManager。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: Medium
  todo_refactor_ddd:
    - Detected runtime IO/external interaction -> infrastructure/container
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/utils/package-manager.ts -> services/n8n/infrastructure/n8n-node-cli/container/utils/package_manager.py

import fs from 'node:fs/promises';

type PackageManager = 'npm' | 'yarn' | 'pnpm';

export function detectPackageManagerFromUserAgent(): PackageManager | null {
	if ('npm_config_user_agent' in process.env) {
		const ua = process.env['npm_config_user_agent'] ?? '';
		if (ua.includes('pnpm')) return 'pnpm';
		if (ua.includes('yarn')) return 'yarn';
		if (ua.includes('npm')) return 'npm';
	}
	return null;
}

async function detectPackageManagerFromLockFiles(): Promise<PackageManager | null> {
	const lockFiles: Record<PackageManager, string> = {
		npm: 'package-lock.json',
		yarn: 'yarn.lock',
		pnpm: 'pnpm-lock.yaml',
	};

	for (const [pm, lockFile] of Object.entries(lockFiles)) {
		try {
			const stats = await fs.stat(lockFile);
			if (stats.isFile()) {
				return pm as PackageManager;
			}
		} catch (e) {
			// File does not exist
		}
	}
	return null;
}

export async function detectPackageManager(): Promise<PackageManager | null> {
	// When used via package.json scripts or `npm/yarn/pnpm create`, we can detect the package manager via the user agent
	const fromUserAgent = detectPackageManagerFromUserAgent();
	if (fromUserAgent) return fromUserAgent;

	// When used directly via `n8n-node` CLI, we can try to detect the package manager via the lock files
	const fromLockFiles = await detectPackageManagerFromLockFiles();
	if (fromLockFiles) return fromLockFiles;

	return null;
}
