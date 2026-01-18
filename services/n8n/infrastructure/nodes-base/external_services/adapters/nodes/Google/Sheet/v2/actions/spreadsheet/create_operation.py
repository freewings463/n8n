"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Sheet/v2/actions/spreadsheet/create.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Sheet 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../utils/utilities、../helpers/GoogleSheets.types、../../transport。导出:description。关键函数/方法:execute、wrapData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Sheet/v2/actions/spreadsheet/create.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Sheet/v2/actions/spreadsheet/create_operation.py

import type { IExecuteFunctions, IDataObject, INodeExecutionData } from 'n8n-workflow';

import { wrapData } from '../../../../../../utils/utilities';
import type { SpreadSheetProperties } from '../../helpers/GoogleSheets.types';
import { apiRequest } from '../../transport';

export const description: SpreadSheetProperties = [
	{
		displayName: 'Title',
		name: 'title',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				resource: ['spreadsheet'],
				operation: ['create'],
			},
		},
		description: 'The title of the spreadsheet',
	},
	{
		displayName: 'Sheets',
		name: 'sheetsUi',
		placeholder: 'Add Sheet',
		type: 'fixedCollection',
		typeOptions: {
			multipleValues: true,
		},
		default: {},
		options: [
			{
				name: 'sheetValues',
				displayName: 'Sheet',
				values: [
					{
						displayName: 'Title',
						name: 'title',
						type: 'string',
						default: '',
						description: 'Title of the property to create',
					},
					{
						displayName: 'Hidden',
						name: 'hidden',
						type: 'boolean',
						default: false,
						description: 'Whether the Sheet should be hidden in the UI',
					},
				],
			},
		],
		displayOptions: {
			show: {
				resource: ['spreadsheet'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		displayOptions: {
			show: {
				resource: ['spreadsheet'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Locale',
				name: 'locale',
				type: 'string',
				default: '',
				placeholder: 'en_US',
				description: `The locale of the spreadsheet in one of the following formats:
				<ul>
					<li>en (639-1)</li>
					<li>fil (639-2 if no 639-1 format exists)</li>
					<li>en_US (combination of ISO language an country)</li>
				<ul>`,
			},
			{
				displayName: 'Recalculation Interval',
				name: 'autoRecalc',
				type: 'options',
				options: [
					{
						name: 'Default',
						value: '',
						description: 'Default value',
					},
					{
						name: 'On Change',
						value: 'ON_CHANGE',
						description: 'Volatile functions are updated on every change',
					},
					{
						name: 'Minute',
						value: 'MINUTE',
						description: 'Volatile functions are updated on every change and every minute',
					},
					{
						name: 'Hour',
						value: 'HOUR',
						description: 'Volatile functions are updated on every change and hourly',
					},
				],
				default: '',
				description: 'Cell recalculation interval options',
			},
		],
	},
];

export async function execute(this: IExecuteFunctions): Promise<INodeExecutionData[]> {
	const items = this.getInputData();
	const returnData: INodeExecutionData[] = [];

	for (let i = 0; i < items.length; i++) {
		const title = this.getNodeParameter('title', i) as string;
		const sheetsUi = this.getNodeParameter('sheetsUi', i, {}) as IDataObject;

		const body = {
			properties: {
				title,
				autoRecalc: undefined as undefined | string,
				locale: undefined as undefined | string,
			},
			sheets: [] as IDataObject[],
		};

		const options = this.getNodeParameter('options', i, {});

		if (Object.keys(sheetsUi).length) {
			const data = [];
			const sheets = sheetsUi.sheetValues as IDataObject[];
			for (const properties of sheets) {
				data.push({ properties });
			}
			body.sheets = data;
		}

		body.properties.autoRecalc = options.autoRecalc ? (options.autoRecalc as string) : undefined;
		body.properties.locale = options.locale ? (options.locale as string) : undefined;

		const response = await apiRequest.call(this, 'POST', '/v4/spreadsheets', body);

		const executionData = this.helpers.constructExecutionMetaData(
			wrapData(response as IDataObject),
			{ itemData: { item: i } },
		);

		returnData.push(...executionData);
	}

	return returnData;
}
