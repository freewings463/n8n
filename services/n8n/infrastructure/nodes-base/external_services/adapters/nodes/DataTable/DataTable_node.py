"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/DataTable/DataTable.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/DataTable 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./actions/router、../row/Row.resource、../table/Table.resource。导出:DataTable。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/DataTable/DataTable.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/DataTable/DataTable_node.py

import type { IExecuteFunctions, INodeType, INodeTypeDescription } from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { router } from './actions/router';
import * as row from './actions/row/Row.resource';
import * as table from './actions/table/Table.resource';
import {
	getConditionsForColumn,
	getDataTableColumns,
	getDataTables,
	tableSearch,
} from './common/methods';

export class DataTable implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Data table',
		name: 'dataTable',
		icon: 'fa:table',
		iconColor: 'orange-red',
		group: ['input', 'transform'],
		version: [1, 1.1],
		subtitle: '={{$parameter["action"]}}',
		description: 'Permanently save data across workflow executions in a table',
		defaults: {
			name: 'Data table',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		hints: [
			{
				message: 'The selected data table has no columns.',
				displayCondition:
					'={{ $parameter.dataTableId !== "" && $parameter?.columns?.mappingMode === "defineBelow" && !$parameter?.columns?.schema?.length }}',
				whenToDisplay: 'beforeExecution',
				location: 'ndv',
				type: 'info',
			},
		],
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Row',
						value: 'row',
					},
					{
						name: 'Table',
						value: 'table',
					},
				],
				default: 'row',
			},
			...row.description,
			...table.description,
		],
	};

	methods = {
		listSearch: {
			tableSearch,
		},
		loadOptions: {
			getDataTableColumns,
			getConditionsForColumn,
		},
		resourceMapping: {
			getDataTables,
		},
	};

	async execute(this: IExecuteFunctions) {
		return await router.call(this);
	}
}
