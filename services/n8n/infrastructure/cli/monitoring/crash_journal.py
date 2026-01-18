"""
MIGRATION-META:
  source_path: packages/cli/src/crash-journal.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src 的模块。导入/依赖:外部:fs/promises；内部:@n8n/backend-common、@n8n/di、n8n-core、n8n-workflow；本地:无。导出:touchFile、init、cleanup。关键函数/方法:init、touchFile、cleanup。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected crash/telemetry/logging IO -> infrastructure/monitoring
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/crash-journal.ts -> services/n8n/infrastructure/cli/monitoring/crash_journal.py

import { inProduction, Logger } from '@n8n/backend-common';
import { Container } from '@n8n/di';
import { existsSync } from 'fs';
import { mkdir, utimes, open, rm } from 'fs/promises';
import { InstanceSettings } from 'n8n-core';
import { sleep } from 'n8n-workflow';
import { join, dirname } from 'path';

export const touchFile = async (filePath: string): Promise<void> => {
	await mkdir(dirname(filePath), { recursive: true });
	const time = new Date();
	try {
		await utimes(filePath, time, time);
	} catch {
		const fd = await open(filePath, 'w');
		await fd.close();
	}
};

const { n8nFolder } = Container.get(InstanceSettings);
const journalFile = join(n8nFolder, 'crash.journal');

export const init = async () => {
	if (!inProduction) return;

	if (existsSync(journalFile)) {
		// Crash detected
		Container.get(Logger).error('Last session crashed');
		// add a 10 seconds pause to slow down crash-looping
		await sleep(10_000);
	}
	await touchFile(journalFile);
};

export const cleanup = async () => {
	await rm(journalFile, { force: true });
};
