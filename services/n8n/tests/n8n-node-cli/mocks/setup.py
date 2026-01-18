"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/test-utils/setup.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/test-utils 的模块。导入/依赖:外部:无；内部:无；本地:./matchers。导出:无。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - CLI test utilities -> tests/mocks
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/test-utils/setup.ts -> services/n8n/tests/n8n-node-cli/mocks/setup.py

import './matchers';

vi.mock('node:child_process');
vi.mock('@clack/prompts', () => ({
	intro: vi.fn(),
	outro: vi.fn(),
	cancel: vi.fn(),
	note: vi.fn(),
	log: {
		success: vi.fn(),
		warning: vi.fn(),
		error: vi.fn(),
		info: vi.fn(),
	},
	spinner: vi.fn(() => ({
		start: vi.fn(),
		stop: vi.fn(),
		message: vi.fn(),
	})),
	confirm: vi.fn(),
	text: vi.fn(),
	select: vi.fn(),
	isCancel: vi.fn(),
}));

vi.spyOn(process, 'exit').mockImplementation((code?: string | number | null) => {
	throw new Error(`EEXIT: ${code ?? 0}`);
});
