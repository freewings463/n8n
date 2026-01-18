"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DataTable/common/addRow.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DataTable/common 的节点。导入/依赖:外部:无；内部:无；本地:./fields、./utils。导出:makeAddRow、getAddRow。关键函数/方法:makeAddRow、getAddRow。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DataTable/common/addRow.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DataTable/common/addRow.py

import {
	DATA_TABLE_SYSTEM_COLUMNS,
	type IDataObject,
	type IDisplayOptions,
	type IExecuteFunctions,
	type INodeProperties,
} from 'n8n-workflow';

import { DATA_TABLE_ID_FIELD } from './fields';
import { dataObjectToApiInput } from './utils';

export function makeAddRow(operation: string, displayOptions: IDisplayOptions) {
	return {
		displayName: 'Columns',
		name: 'columns',
		type: 'resourceMapper',
		default: {
			mappingMode: 'defineBelow',
			value: null,
		},
		noDataExpression: true,
		required: true,
		typeOptions: {
			loadOptionsDependsOn: [`${DATA_TABLE_ID_FIELD}.value`],
			resourceMapper: {
				valuesLabel: `Values to ${operation}`,
				resourceMapperMethod: 'getDataTables',
				mode: 'add',
				fieldWords: {
					singular: 'column',
					plural: 'columns',
				},
				addAllFields: true,
				multiKeyMatch: true,
				hideNoDataError: true,
			},
		},
		displayOptions,
	} satisfies INodeProperties;
}

export function getAddRow(ctx: IExecuteFunctions, index: number) {
	const items = ctx.getInputData();
	const dataMode = ctx.getNodeParameter('columns.mappingMode', index) as string;

	let data: IDataObject;

	if (dataMode === 'autoMapInputData') {
		data = { ...items[index].json };
		// We automatically remove our system columns for better UX when feeding data table outputs
		// into another data table node
		for (const systemColumn of DATA_TABLE_SYSTEM_COLUMNS) {
			delete data[systemColumn];
		}
	} else {
		const fields = ctx.getNodeParameter('columns.value', index, {}) as IDataObject;

		data = fields;
	}

	return dataObjectToApiInput(data, ctx.getNode(), index);
}
