"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DataTable/actions/row/upsert.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DataTable/actions 的节点。导入/依赖:外部:无；内部:无；本地:../common/addRow、../common/fields、../common/selectMany、../common/utils。导出:FIELD、description。关键函数/方法:execute、makeAddRow。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DataTable/actions/row/upsert.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DataTable/actions/row/upsert_operation.py

import {
	NodeOperationError,
	type IDisplayOptions,
	type IExecuteFunctions,
	type INodeExecutionData,
	type INodeProperties,
} from 'n8n-workflow';

import { makeAddRow, getAddRow } from '../../common/addRow';
import { DRY_RUN } from '../../common/fields';
import { getSelectFields, getSelectFilter } from '../../common/selectMany';
import { getDataTableProxyExecute, getDryRunParameter } from '../../common/utils';

export const FIELD: string = 'upsert';

const displayOptions: IDisplayOptions = {
	show: {
		resource: ['row'],
		operation: [FIELD],
	},
};

export const description: INodeProperties[] = [
	...getSelectFields(displayOptions),
	makeAddRow(FIELD, displayOptions),
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		default: {},
		placeholder: 'Add option',
		options: [DRY_RUN],
		displayOptions,
	},
];

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const dataTableProxy = await getDataTableProxyExecute(this, index);
	const dryRun = getDryRunParameter(this, index);
	const row = getAddRow(this, index);
	const filter = await getSelectFilter(this, index);

	if (filter.filters.length === 0) {
		throw new NodeOperationError(this.getNode(), 'At least one condition is required');
	}

	const result = await dataTableProxy.upsertRow({
		data: row,
		filter,
		dryRun,
	});

	return result.map((json) => ({ json }));
}
