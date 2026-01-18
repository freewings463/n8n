"""
MIGRATION-META:
  source_path: packages/@n8n/benchmark/scripts/n8n-setups/scaling-multi-main/setup.mjs
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/benchmark/scripts/n8n-setups/scaling-multi-main 的模块。导入/依赖:外部:zx；内部:无；本地:无。导出:setup。关键函数/方法:setup。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Benchmark scripts -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/benchmark/scripts/n8n-setups/scaling-multi-main/setup.mjs -> services/n8n/infrastructure/n8n-benchmark/container/bin/benchmark/n8n-setups/scaling-multi-main/setup.py

#!/usr/bin/env zx

import path from 'path';
import { fs } from 'zx';

/**
 * Creates the needed directories so the permissions get set correctly.
 */
export function setup({ runDir }) {
	const neededDirs = ['n8n-worker1', 'n8n-worker2', 'n8n-main1', 'n8n-main2', 'postgres'];

	for (const dir of neededDirs) {
		fs.ensureDirSync(path.join(runDir, dir));
	}
}
