"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/test-utils/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/test-utils 的入口。导入/依赖:外部:无；内部:无；本地:无。导出:CommandTester、type CommandResult、type LogLevel、tmpdirTest、MockPrompt、setupTestPackage、type PackageSetupOptions。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - CLI test utilities -> tests/mocks
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/test-utils/index.ts -> services/n8n/tests/n8n-node-cli/mocks/__init__.py

export { CommandTester, type CommandResult, type LogLevel } from './command-tester';
export {
	mockSpawn,
	mockExecSync,
	type MockChildProcess,
	type MockSpawnOptions,
	type CommandMockConfig,
	type ExecSyncMockConfig,
} from './mock-child-process';
export { tmpdirTest } from './temp-fs';
export { MockPrompt } from './mock-prompts';
export { setupTestPackage, type PackageSetupOptions } from './package-setup';
