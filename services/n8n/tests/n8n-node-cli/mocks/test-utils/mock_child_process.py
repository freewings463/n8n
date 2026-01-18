"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/test-utils/mock-child-process.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/test-utils 的模块。导入/依赖:外部:node:child_process；内部:无；本地:无。导出:MockChildProcess、MockSpawnOptions、CommandMockConfig、mockSpawn、ExecSyncMockConfig、mockExecSync。关键函数/方法:createMockProcess、emitProcessEvents、setImmediate、mockSpawn、expect、mockExecSync。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/test-utils/mock-child-process.ts -> services/n8n/tests/n8n-node-cli/mocks/test-utils/mock_child_process.py

import { spawn, execSync, type ChildProcess } from 'node:child_process';
import { EventEmitter } from 'node:events';

export interface MockChildProcess extends EventEmitter {
	stdout: EventEmitter | null;
	stderr: EventEmitter | null;
}

export interface MockSpawnOptions {
	exitCode?: number;
	signal?: NodeJS.Signals;
	stdout?: string;
	stderr?: string;
	error?: string;
}

export interface CommandMockConfig {
	command: string;
	args: string[];
	options?: MockSpawnOptions;
}

function createMockProcess(): ChildProcess {
	const emitter = new EventEmitter();
	const mockProcess: MockChildProcess = Object.assign(emitter, {
		stdout: new EventEmitter(),
		stderr: new EventEmitter(),
	});
	return mockProcess as unknown as ChildProcess;
}

function emitProcessEvents(mockProcess: MockChildProcess, options: MockSpawnOptions): void {
	const {
		exitCode = options.signal ? null : 0,
		signal = null,
		stdout = '',
		stderr = '',
		error,
	} = options;

	setImmediate(() => {
		if (error) {
			mockProcess.emit('error', new Error(error));
			setImmediate(() => {
				mockProcess.emit('close', exitCode !== 0 ? exitCode : 1, signal);
			});
			return;
		}

		if (stdout && mockProcess.stdout) {
			mockProcess.stdout.emit('data', Buffer.from(stdout));
		}
		if (stderr && mockProcess.stderr) {
			mockProcess.stderr.emit('data', Buffer.from(stderr));
		}

		mockProcess.emit('close', exitCode, signal);
	});
}

export function mockSpawn(command: string, args: string[], options?: MockSpawnOptions): void;
export function mockSpawn(commands: CommandMockConfig[]): void;
export function mockSpawn(
	commandOrCommands: string | CommandMockConfig[],
	args?: string[],
	options?: MockSpawnOptions,
): void {
	if (Array.isArray(commandOrCommands)) {
		const commands = commandOrCommands;
		let callIndex = 0;

		vi.mocked(spawn).mockImplementation((cmd, cmdArgs): ChildProcess => {
			if (callIndex >= commands.length) {
				throw new Error(`Unexpected spawn call: ${cmd} ${cmdArgs?.join(' ')}`);
			}

			const expectedConfig = commands[callIndex];
			expect(cmd).toBe(expectedConfig.command);
			expect(cmdArgs).toEqual(expectedConfig.args);

			const mockProcess = createMockProcess();
			const options = expectedConfig.options ?? {};

			emitProcessEvents(mockProcess, options);

			callIndex++;
			return mockProcess;
		});
	} else {
		const command = commandOrCommands;
		if (!args) throw new Error('args required for single command mock');

		vi.mocked(spawn).mockImplementation((cmd, cmdArgs): ChildProcess => {
			expect(cmd).toBe(command);
			expect(cmdArgs).toEqual(args);

			const mockProcess = createMockProcess();
			const mockOptions = options ?? {};

			emitProcessEvents(mockProcess, mockOptions);

			return mockProcess;
		});
	}
}

export interface ExecSyncMockConfig {
	command: string;
	result: string;
}

export function mockExecSync(configs: ExecSyncMockConfig[]): void {
	const configMap = new Map(configs.map((c) => [c.command, c.result]));

	vi.mocked(execSync).mockImplementation((command) => {
		const result = configMap.get(String(command));
		if (result === undefined) {
			throw new Error(`Unexpected execSync call: ${command}`);
		}
		return Buffer.from(result);
	});
}
