"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Simulate/methods/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Simulate/methods 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:getNodeTypes。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Simulate/methods/loadOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Simulate/methods/loadOptions.py

import type { ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';

export async function getNodeTypes(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const types = this.getKnownNodeTypes() as {
		[key: string]: {
			className: string;
		};
	};

	const returnData: INodePropertyOptions[] = [];

	let typeNames = Object.keys(types);

	if (this.getNode().type === 'n8n-nodes-base.simulateTrigger') {
		typeNames = typeNames.filter((type) => type.toLowerCase().includes('trigger'));
	}

	for (const type of typeNames) {
		returnData.push({
			name: types[type].className,
			value: type,
		});
	}

	return returnData;
}
