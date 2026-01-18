"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DataTable/actions/table/delete.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DataTable/actions 的节点。导入/依赖:外部:无；内部:无；本地:../common/fields、../common/utils。导出:FIELD、description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DataTable/actions/table/delete.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DataTable/actions/table/delete_operation.py

import type {
	IDisplayOptions,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { DATA_TABLE_ID_FIELD } from '../../common/fields';
import { getDataTableProxyExecute } from '../../common/utils';

export const FIELD = 'delete';

const displayOptions: IDisplayOptions = {
	show: {
		resource: ['table'],
		operation: [FIELD],
	},
};

export const description: INodeProperties[] = [
	{
		displayName:
			'This will permanently delete the data table and all its data. This action cannot be undone.',
		name: 'deleteWarning',
		type: 'notice',
		default: '',
		displayOptions,
	},
];

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const dataTableId = this.getNodeParameter(DATA_TABLE_ID_FIELD, index, undefined, {
		extractValue: true,
	}) as string;

	const dataTableProxy = await getDataTableProxyExecute(this, index);

	const success = await dataTableProxy.deleteDataTable();

	return [{ json: { success, deletedTableId: dataTableId } }];
}
