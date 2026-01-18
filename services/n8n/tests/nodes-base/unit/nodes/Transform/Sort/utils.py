"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Transform/Sort/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Transform/Sort 的节点。导入/依赖:外部:无；内部:@n8n/vm2、n8n-workflow；本地:无。导出:sortByCode。关键函数/方法:sortByCode。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Transform/Sort/utils.ts -> services/n8n/tests/nodes-base/unit/nodes/Transform/Sort/utils.py

import { NodeVM } from '@n8n/vm2';
import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

const returnRegExp = /\breturn\b/;
export function sortByCode(
	this: IExecuteFunctions,
	items: INodeExecutionData[],
): INodeExecutionData[] {
	const code = this.getNodeParameter('code', 0) as string;
	if (!returnRegExp.test(code)) {
		throw new NodeOperationError(
			this.getNode(),
			"Sort code doesn't return. Please add a 'return' statement to your code",
		);
	}

	const mode = this.getMode();
	const vm = new NodeVM({
		console: mode === 'manual' ? 'redirect' : 'inherit',
		sandbox: { items },
	});

	return vm.run(`module.exports = items.sort((a, b) => { ${code} })`);
}
