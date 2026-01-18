"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/test-utils/command-tester.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/test-utils 的模块。导入/依赖:外部:@clack/prompts、@oclif/core、vitest-mock-extended；内部:无；本地:../index。导出:LogLevel、CommandResult、CommandTester。关键函数/方法:run、isValidCommand、getLogMessages。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - CLI test utilities -> tests/mocks
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/test-utils/command-tester.ts -> services/n8n/tests/n8n-node-cli/mocks/command_tester.py

import { log } from '@clack/prompts';
import type { Config } from '@oclif/core';
import { mock } from 'vitest-mock-extended';

import { commands } from '../index';

function isValidCommand(commandName: string): commandName is keyof typeof commands {
	return commandName in commands;
}

export type LogLevel = 'success' | 'warning' | 'error' | 'info';

export interface CommandResult {
	getLogMessages(type: LogLevel): string[];
}

export class CommandTester {
	static async run(commandLine: string): Promise<CommandResult> {
		const argv = commandLine.trim().split(/\s+/);
		const [commandName, ...restArgv] = argv;

		if (!isValidCommand(commandName)) {
			throw new Error(
				`Unknown command: ${commandName}. Available: ${Object.keys(commands).join(', ')}`,
			);
		}

		const CommandClass = commands[commandName];

		const command = new CommandClass(
			restArgv,
			mock<Config>({
				root: process.cwd(),
				name: '@n8n/node-cli',
				version: '1.0.0',
				runHook: async () => await Promise.resolve({ successes: [], failures: [] }),
			}),
		);

		await command.run();

		return {
			getLogMessages(type: LogLevel): string[] {
				const mockFn = vi.mocked(log[type]);
				return mockFn.mock.calls?.map((call) => call[0]) ?? [];
			},
		};
	}
}
