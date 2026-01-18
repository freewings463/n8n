"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Merge/v3/methods/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Merge/v3 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:无。关键函数/方法:getResolveClashOptions、getInputs。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Merge/v3/methods/loadOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Merge/v3/methods/loadOptions.py

import type { ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';

export async function getResolveClashOptions(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const numberOfInputs = this.getNodeParameter('numberInputs', 2) as number;

	if (numberOfInputs <= 2) {
		return [
			{
				name: 'Always Add Input Number to Field Names',
				value: 'addSuffix',
			},
			{
				name: 'Prefer Input 1 Version',
				value: 'preferInput1',
			},
			{
				name: 'Prefer Input 2 Version',
				value: 'preferLast',
			},
		];
	} else {
		return [
			{
				name: 'Always Add Input Number to Field Names',
				value: 'addSuffix',
			},
			{
				name: 'Use Earliest Version',
				value: 'preferInput1',
			},
		];
	}
}
export async function getInputs(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const numberOfInputs = this.getNodeParameter('numberInputs', 2) as number;

	const returnData: INodePropertyOptions[] = [];

	for (let i = 0; i < numberOfInputs; i++) {
		returnData.push({
			name: `${i + 1}`,
			value: i + 1,
		});
	}

	return returnData;
}
