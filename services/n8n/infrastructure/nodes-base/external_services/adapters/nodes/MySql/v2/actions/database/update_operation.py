"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MySql/v2/actions/database/update.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MySql/v2 的节点。导入/依赖:外部:@utils/utilities；内部:无；本地:../helpers/interfaces、../helpers/utils、../common.descriptions。导出:description。关键函数/方法:execute、valuesToSend。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MySql/v2/actions/database/update.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MySql/v2/actions/database/update_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import type { QueryRunner, QueryValues, QueryWithValues } from '../../helpers/interfaces';
import { AUTO_MAP, DATA_MODE } from '../../helpers/interfaces';
import { escapeSqlIdentifier, replaceEmptyStringsByNulls } from '../../helpers/utils';
import { optionsCollection } from '../common.descriptions';

const properties: INodeProperties[] = [
	{
		displayName: 'Data Mode',
		name: 'dataMode',
		type: 'options',
		options: [
			{
				name: 'Auto-Map Input Data to Columns',
				value: DATA_MODE.AUTO_MAP,
				description: 'Use when node input properties names exactly match the table column names',
			},
			{
				name: 'Map Each Column Below',
				value: DATA_MODE.MANUAL,
				description: 'Set the value for each destination column manually',
			},
		],
		default: AUTO_MAP,
		description:
			'Whether to map node input properties and the table data automatically or manually',
	},
	{
		displayName: `
		In this mode, make sure incoming data fields are named the same as the columns in your table. If needed, use an 'Edit Fields' node before this node to change the field names.
		`,
		name: 'notice',
		type: 'notice',
		default: '',
		displayOptions: {
			show: {
				dataMode: [DATA_MODE.AUTO_MAP],
			},
		},
	},
	{
		// eslint-disable-next-line n8n-nodes-base/node-param-display-name-wrong-for-dynamic-options
		displayName: 'Column to Match On',
		name: 'columnToMatchOn',
		type: 'options',
		required: true,
		// eslint-disable-next-line n8n-nodes-base/node-param-description-wrong-for-dynamic-options
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/" target="_blank">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getColumns',
			loadOptionsDependsOn: ['schema.value', 'table.value'],
		},
		default: '',
		hint: "Used to find the correct row to update. Doesn't get changed.",
	},
	{
		displayName: 'Value of Column to Match On',
		name: 'valueToMatchOn',
		type: 'string',
		default: '',
		description:
			'Rows with a value in the specified "Column to Match On" that corresponds to the value in this field will be updated',
		displayOptions: {
			show: {
				dataMode: [DATA_MODE.MANUAL],
			},
		},
	},
	{
		displayName: 'Values to Send',
		name: 'valuesToSend',
		placeholder: 'Add Value',
		type: 'fixedCollection',
		typeOptions: {
			multipleValueButtonText: 'Add Value',
			multipleValues: true,
		},
		displayOptions: {
			show: {
				dataMode: [DATA_MODE.MANUAL],
			},
		},
		default: {},
		options: [
			{
				displayName: 'Values',
				name: 'values',
				values: [
					{
						// eslint-disable-next-line n8n-nodes-base/node-param-display-name-wrong-for-dynamic-options
						displayName: 'Column',
						name: 'column',
						type: 'options',
						// eslint-disable-next-line n8n-nodes-base/node-param-description-wrong-for-dynamic-options
						description:
							'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/" target="_blank">expression</a>',
						typeOptions: {
							loadOptionsMethod: 'getColumnsWithoutColumnToMatchOn',
							loadOptionsDependsOn: ['schema.value', 'table.value'],
						},
						default: [],
					},
					{
						displayName: 'Value',
						name: 'value',
						type: 'string',
						default: '',
					},
				],
			},
		],
	},
	optionsCollection,
];

const displayOptions = {
	show: {
		resource: ['database'],
		operation: ['update'],
	},
	hide: {
		table: [''],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	inputItems: INodeExecutionData[],
	runQueries: QueryRunner,
	nodeOptions: IDataObject,
): Promise<INodeExecutionData[]> {
	let returnData: INodeExecutionData[] = [];
	const items = replaceEmptyStringsByNulls(inputItems, nodeOptions.replaceEmptyStrings as boolean);

	const queries: QueryWithValues[] = [];

	for (let i = 0; i < items.length; i++) {
		const table = this.getNodeParameter('table', i, undefined, {
			extractValue: true,
		}) as string;

		const columnToMatchOn = this.getNodeParameter('columnToMatchOn', i) as string;

		const dataMode = this.getNodeParameter('dataMode', i) as string;

		let item: IDataObject = {};
		let valueToMatchOn: string | IDataObject = '';

		if (dataMode === DATA_MODE.AUTO_MAP) {
			item = items[i].json;
			valueToMatchOn = item[columnToMatchOn] as string;
		}

		if (dataMode === DATA_MODE.MANUAL) {
			const valuesToSend = (this.getNodeParameter('valuesToSend', i, []) as IDataObject)
				.values as IDataObject[];

			item = valuesToSend.reduce((acc, { column, value }) => {
				acc[column as string] = value;
				return acc;
			}, {} as IDataObject);

			valueToMatchOn = this.getNodeParameter('valueToMatchOn', i) as string;
		}

		const values: QueryValues = [];

		const updateColumns = Object.keys(item).filter((column) => column !== columnToMatchOn);

		const updates: string[] = [];

		for (const column of updateColumns) {
			updates.push(`${escapeSqlIdentifier(column)} = ?`);
			values.push(item[column] as string);
		}

		const condition = `${escapeSqlIdentifier(columnToMatchOn)} = ?`;
		values.push(valueToMatchOn);

		const query = `UPDATE ${escapeSqlIdentifier(table)} SET ${updates.join(
			', ',
		)} WHERE ${condition}`;

		queries.push({ query, values });
	}

	returnData = await runQueries(queries);

	return returnData;
}
