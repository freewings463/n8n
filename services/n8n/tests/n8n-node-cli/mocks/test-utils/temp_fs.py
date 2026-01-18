"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/test-utils/temp-fs.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/test-utils 的模块。导入/依赖:外部:node:fs/promises、vitest；内部:无；本地:无。导出:tmpdirTest。关键函数/方法:createTempDir。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/test-utils/temp-fs.ts -> services/n8n/tests/n8n-node-cli/mocks/test-utils/temp_fs.py

import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { test } from 'vitest';

async function createTempDir(): Promise<string> {
	const ostmpdir = os.tmpdir();
	const tmpdir = path.join(ostmpdir, 'n8n-node-cli-test-');
	return await fs.mkdtemp(tmpdir);
}

interface TmpDirFixture {
	tmpdir: string;
}

export const tmpdirTest = test.extend<TmpDirFixture>({
	tmpdir: async ({ expect: _expect }, use) => {
		const directory = await createTempDir();
		const originalCwd = process.cwd();

		process.chdir(directory);

		try {
			await use(directory);
		} finally {
			process.chdir(originalCwd);
			await fs.rm(directory, { recursive: true, force: true });
		}
	},
});
