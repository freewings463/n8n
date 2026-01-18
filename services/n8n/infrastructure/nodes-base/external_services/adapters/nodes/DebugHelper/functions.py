"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DebugHelper/functions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DebugHelper 的节点。导入/依赖:外部:v8、vm；内部:无；本地:无。导出:runGarbageCollector、generateGarbageMemory。关键函数/方法:runGarbageCollector、setFlagsFromString、gc、generateGarbageMemory。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DebugHelper/functions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DebugHelper/functions.py

import { setFlagsFromString } from 'v8';
import { runInNewContext } from 'vm';

export const runGarbageCollector = () => {
	try {
		setFlagsFromString('--expose_gc');
		const gc = runInNewContext('gc'); // nocommit
		gc();
	} catch (error) {
		console.error(error);
	}
};

export const generateGarbageMemory = (sizeInMB: number, onHeap = true) => {
	const divider = onHeap ? 8 : 1;
	const size = Math.max(1, Math.floor((sizeInMB * 1024 * 1024) / divider));
	if (onHeap) {
		// arrays are allocated on the heap
		// size in this case is only an approximation...
		const array = Array(size);
		array.fill(0);
	} else {
		const array = new Uint8Array(size);
		array.fill(0);
	}
	return { ...process.memoryUsage() };
};
