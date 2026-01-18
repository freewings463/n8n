"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SeaTable/v2/actions/link/add.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SeaTable/v2 的节点。导入/依赖:外部:无；内部:无；本地:../../GenericFunctions。导出:properties、description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SeaTable/v2/actions/link/add.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SeaTable/v2/actions/link/add_operation.py

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
		// eslint-disable-next-line n8n-nodes-base/node-param-display-name-wrong-for-dynamic-options
		displayName: 'Table Name (Source)',
		name: 'tableName',
		type: 'options',
		placeholder: 'Name of table',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getTableNameAndId',
		},
		default: '',
		// eslint-disable-next-line n8n-nodes-base/node-param-description-wrong-for-dynamic-options
		description:
			'Choose from the list, of specify by using an expression. Provide it in the way "table_name:::table_id".',
	},
	{
		// eslint-disable-next-line n8n-nodes-base/node-param-display-name-wrong-for-dynamic-options
		displayName: 'Link Column',
		name: 'linkColumn',
		type: 'options',
		typeOptions: {
			loadOptionsDependsOn: ['tableName'],
			loadOptionsMethod: 'getLinkColumns',
		},
		required: true,
		default: '',
		// eslint-disable-next-line n8n-nodes-base/node-param-description-wrong-for-dynamic-options
		description:
			'Choose from the list of specify the Link Column by using an expression. You have to provide it in the way "column_name:::link_id:::other_table_id".',
	},
	{
		displayName: 'Row ID From the Source Table',
		name: 'linkColumnSourceId',
		type: 'string',
		required: true,
		default: '',
		description: 'Provide the row ID of table you selected',
	},
	{
		displayName: 'Row ID From the Target',
		name: 'linkColumnTargetId',
		type: 'string',
		required: true,
		default: '',
		description: 'Provide the row ID of table you want to link',
	},
];

const displayOptions = {
	show: {
		resource: ['link'],
		operation: ['add'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const tableName = this.getNodeParameter('tableName', index) as string;
	const linkColumn = this.getNodeParameter('linkColumn', index) as any;
	const linkColumnSourceId = this.getNodeParameter('linkColumnSourceId', index) as string;
	const linkColumnTargetId = this.getNodeParameter('linkColumnTargetId', index) as string;

	const body = {
		link_id: linkColumn.split(':::')[1],
		table_id: tableName.split(':::')[1],
		other_table_id: linkColumn.split(':::')[2],
		other_rows_ids_map: {
			[linkColumnSourceId]: [linkColumnTargetId],
		},
	};

	const responseData = await seaTableApiRequest.call(
		this,
		{},
		'POST',
		'/api-gateway/api/v2/dtables/{{dtable_uuid}}/links/',
		body,
	);

	return this.helpers.returnJsonArray(responseData as IDataObject[]);
}
