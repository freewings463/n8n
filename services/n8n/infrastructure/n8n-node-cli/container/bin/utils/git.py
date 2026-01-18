"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/utils/git.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/utils 的工具。导入/依赖:外部:node:child_process；内部:无；本地:./child-process。导出:tryReadGitUser。关键函数/方法:tryReadGitUser、initGit。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected child_process execution -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/utils/git.ts -> services/n8n/infrastructure/n8n-node-cli/container/bin/utils/git.py

import { execSync } from 'node:child_process';

import { runCommand } from './child-process';

type GitUser = {
	name?: string;
	email?: string;
};

export function tryReadGitUser(): GitUser {
	const user: GitUser = { name: '', email: '' };

	try {
		const name = execSync('git config --get user.name', {
			stdio: ['pipe', 'pipe', 'ignore'],
		})
			.toString()
			.trim();
		if (name) user.name = name;
	} catch {
		// ignore
	}

	try {
		const email = execSync('git config --get user.email', {
			stdio: ['pipe', 'pipe', 'ignore'],
		})
			.toString()
			.trim();
		if (email) user.email = email;
	} catch {
		// ignore
	}

	return user;
}

export async function initGit(dir: string): Promise<void> {
	await runCommand('git', ['init', '-b', 'main'], { cwd: dir });
}
