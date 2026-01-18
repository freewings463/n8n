"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v2/actions/link/list.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v2 的节点。导入/依赖:外部:无；内部:无；本地:../../GenericFunctions。导出:properties、description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-param-display-name-wrong-for-dynamic-options。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v2/actions/link/list.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v2/actions/link/list_operation.py

/* eslint-disable n8n-nodes-base/node-param-display-name-wrong-for-dynamic-options */
/* eslint-disable n8n-nodes-base/node-param-description-wrong-for-dynamic-options */
import {
	type IDataObject,
	type INodeExecutionData,
	type INodeProperties,
	type IExecuteFunctions,
	updateDisplayOptions,
} from 'n8n-workflow';

import { seaTableApiRequest } from '../../GenericFunctions';

export const properties: INodeProperties[] = [
	{
		displayName: 'Table Name',
		name: 'tableName',
		type: 'options',
		placeholder: 'Select a table',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getTableNameAndId',
		},
		default: '',
		description:
			'Choose from the list, of specify by using an expression. Provide it in the way "table_name:::table_id".',
	},
	{
		displayName: 'Link Column',
		name: 'linkColumn',
		type: 'options',
		typeOptions: {
			loadOptionsDependsOn: ['tableName'],
			loadOptionsMethod: 'getLinkColumnsWithColumnKey',
		},
		required: true,
		default: '',
		description:
			'Choose from the list of specify the Link Column by using an expression. You have to provide it in the way "column_name:::link_id:::other_table_id:::column_key".',
	},
	{
		displayName: 'Row ID',
		name: 'rowId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		required: true,
		typeOptions: {
			loadOptionsDependsOn: ['tableName'],
			loadOptionsMethod: 'getRowIds',
		},
		default: '',
	},
];

const displayOptions = {
	show: {
		resource: ['link'],
		operation: ['list'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	// get parameters
	const tableName = this.getNodeParameter('tableName', index) as string;
	const linkColumn = this.getNodeParameter('linkColumn', index) as string;
	const rowId = this.getNodeParameter('rowId', index) as string;

	// get rows
	const responseData = await seaTableApiRequest.call(
		this,
		{},
		'POST',
		'/api-gateway/api/v2/dtables/{{dtable_uuid}}/query-links/',
		{
			table_id: tableName.split(':::')[1],
			link_column_key: linkColumn.split(':::')[3],
			rows: [
				{
					row_id: rowId,
					offset: 0,
					limit: 100,
				},
			],
		},
	);
	return this.helpers.returnJsonArray(responseData as IDataObject[]);
}
