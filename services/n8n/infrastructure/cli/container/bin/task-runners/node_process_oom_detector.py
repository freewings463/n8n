"""
MIGRATION-META:
  source_path: packages/cli/src/task-runners/node-process-oom-detector.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/cli/src/task-runners 的模块。导入/依赖:外部:node:assert/strict、node:child_process；内部:无；本地:无。导出:NodeProcessOomDetector。关键函数/方法:monitorProcess。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected child_process execution -> infrastructure/container/bin
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/cli/src/task-runners/node-process-oom-detector.ts -> services/n8n/infrastructure/cli/container/bin/task-runners/node_process_oom_detector.py

import * as a from 'node:assert/strict';
import type { ChildProcess } from 'node:child_process';

/**
 * Class to monitor a nodejs process and detect if it runs out of
 * memory (OOMs).
 */
export class NodeProcessOomDetector {
	get didProcessOom() {
		return this._didProcessOom;
	}

	private _didProcessOom = false;

	constructor(processToMonitor: ChildProcess) {
		this.monitorProcess(processToMonitor);
	}

	private monitorProcess(processToMonitor: ChildProcess) {
		a.ok(processToMonitor.stderr, "Can't monitor a process without stderr");

		processToMonitor.stderr.on('data', this.onStderr);

		processToMonitor.once('exit', () => {
			processToMonitor.stderr?.off('data', this.onStderr);
		});
	}

	private onStderr = (data: Buffer) => {
		if (data.includes('JavaScript heap out of memory')) {
			this._didProcessOom = true;
		}
	};
}
