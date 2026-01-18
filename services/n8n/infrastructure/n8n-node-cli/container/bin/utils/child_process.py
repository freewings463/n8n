"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/utils/child-process.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/utils 的工具。导入/依赖:外部:node:child_process；内部:无；本地:./package-manager。导出:ChildProcessError。关键函数/方法:runCommand、packageManager、printOutput、reject、resolve。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected child_process execution -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/utils/child-process.ts -> services/n8n/infrastructure/n8n-node-cli/container/bin/utils/child_process.py

import { spawn, type SpawnOptions, type StdioOptions } from 'node:child_process';

import { detectPackageManager } from './package-manager';

export class ChildProcessError extends Error {
	constructor(
		message: string,
		public code: number | null,
		public signal: NodeJS.Signals | null,
	) {
		super(message);
	}
}

export async function runCommand(
	cmd: string,
	args: string[] = [],
	opts: {
		cwd?: string;
		env?: NodeJS.ProcessEnv;
		stdio?: StdioOptions;
		context?: 'local' | 'global';
		printOutput?: (options: { stdout: Buffer[]; stderr: Buffer[] }) => void;
		alwaysPrintOutput?: boolean;
	} = {},
): Promise<void> {
	const packageManager = (await detectPackageManager()) ?? 'npm';

	return await new Promise((resolve, reject) => {
		const options: SpawnOptions = {
			cwd: opts.cwd,
			env: { ...process.env, ...opts.env },
			stdio: opts.stdio ?? ['ignore', 'pipe', 'pipe'],
			shell: process.platform === 'win32',
		};
		const child =
			opts.context === 'local'
				? spawn(packageManager, ['exec', '--', cmd, ...args], options)
				: spawn(cmd, args, options);

		const stdoutBuffers: Buffer[] = [];
		const stderrBuffers: Buffer[] = [];

		child.stdout?.on('data', (data: Buffer) => {
			stdoutBuffers.push(data);
		});
		child.stderr?.on('data', (data: Buffer) => {
			stderrBuffers.push(data);
		});

		function printOutput() {
			if (opts.printOutput) {
				opts.printOutput({ stdout: stdoutBuffers, stderr: stderrBuffers });
				return;
			}
			for (const buffer of stdoutBuffers) {
				process.stdout.write(buffer);
			}
			for (const buffer of stderrBuffers) {
				process.stderr.write(buffer);
			}
		}

		child.on('error', (error) => {
			printOutput();
			reject(new ChildProcessError(error.message, null, null));
		});

		child.on('close', (code, signal) => {
			if (code === 0) {
				// Only print output on success if alwaysPrintOutput is true
				if (opts.alwaysPrintOutput) {
					printOutput();
				}
				resolve();
			} else {
				printOutput();
				reject(
					new ChildProcessError(
						`${cmd} exited with code ${code}${signal ? ` (signal: ${signal})` : ''}`,
						code,
						signal,
					),
				);
			}
		});
	});
}
