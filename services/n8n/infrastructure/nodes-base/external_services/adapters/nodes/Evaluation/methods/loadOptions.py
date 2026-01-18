"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Evaluation/methods/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Evaluation/methods 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../methods/loadOptions。导出:getConditionsForColumn、getDataTableColumns。关键函数/方法:getSheetHeaderRowWithGeneratedColumnNames。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Evaluation/methods/loadOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Evaluation/methods/loadOptions.py

import type { ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';

import { getSheetHeaderRow } from '../../Google/Sheet/v2/methods/loadOptions';
export { getConditionsForColumn, getDataTableColumns } from '../../DataTable/common/methods';

export async function getSheetHeaderRowWithGeneratedColumnNames(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData = await getSheetHeaderRow.call(this);
	return returnData.map((column, i) => {
		if (column.value !== '') return column;
		const indexBasedValue = `col_${i + 1}`;
		return {
			name: indexBasedValue,
			value: indexBasedValue,
		};
	});
}
