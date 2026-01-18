"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v2/actions/row/lock.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../GenericFunctions。导出:无。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v2/actions/row/lock.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v2/actions/row/lock_operation.py

import type { IDataObject, INodeExecutionData, IExecuteFunctions } from 'n8n-workflow';

import { seaTableApiRequest } from '../../GenericFunctions';

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const tableName = this.getNodeParameter('tableName', index) as string;
	const rowId = this.getNodeParameter('rowId', index) as string;

	const responseData = await seaTableApiRequest.call(
		this,
		{},
		'PUT',
		'/api-gateway/api/v2/dtables/{{dtable_uuid}}/lock-rows/',
		{
			table_name: tableName,
			row_ids: [rowId],
		},
	);

	return this.helpers.returnJsonArray(responseData as IDataObject[]);
}
