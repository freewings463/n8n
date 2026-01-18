"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Sheet/v2/actions/sheet/create.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Sheet 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../utils/utilities、../helpers/GoogleSheet、../helpers/GoogleSheets.types、../helpers/GoogleSheets.utils 等1项。导出:description。关键函数/方法:execute、wrapData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Sheet/v2/actions/sheet/create.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Sheet/v2/actions/sheet/create_operation.py

import type { IExecuteFunctions, IDataObject, INodeExecutionData } from 'n8n-workflow';

import { wrapData } from '../../../../../../utils/utilities';
import type { GoogleSheet } from '../../helpers/GoogleSheet';
import type { SheetProperties } from '../../helpers/GoogleSheets.types';
import { getExistingSheetNames, hexToRgb } from '../../helpers/GoogleSheets.utils';
import { apiRequest } from '../../transport';

export const description: SheetProperties = [
	{
		displayName: 'Title',
		name: 'title',
		type: 'string',
		required: true,
		default: 'n8n-sheet',
		displayOptions: {
			show: {
				resource: ['sheet'],
				operation: ['create'],
			},
		},
		description: 'The name of the sheet',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		displayOptions: {
			show: {
				resource: ['sheet'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Hidden',
				name: 'hidden',
				type: 'boolean',
				default: false,
				description: "Whether the sheet is hidden in the UI, false if it's visible",
			},
			{
				displayName: 'Right To Left',
				name: 'rightToLeft',
				type: 'boolean',
				default: false,
				description: 'Whether the sheet is an RTL sheet instead of an LTR sheet',
			},
			{
				displayName: 'Sheet ID',
				name: 'sheetId',
				type: 'number',
				default: 0,
				description:
					'The ID of the sheet. Must be non-negative. This field cannot be changed once set.',
			},
			{
				displayName: 'Sheet Index',
				name: 'index',
				type: 'number',
				default: 0,
				description: 'The index of the sheet within the spreadsheet',
			},
			{
				displayName: 'Tab Color',
				name: 'tabColor',
				type: 'color',
				default: '0aa55c',
				description: 'The color of the tab in the UI',
			},
		],
	},
];

export async function execute(
	this: IExecuteFunctions,
	sheet: GoogleSheet,
	sheetName: string,
): Promise<INodeExecutionData[]> {
	let responseData;
	const returnData: INodeExecutionData[] = [];
	const items = this.getInputData();

	const existingSheetNames = await getExistingSheetNames(sheet);

	for (let i = 0; i < items.length; i++) {
		const sheetTitle = this.getNodeParameter('title', i, {}) as string;

		if (existingSheetNames.includes(sheetTitle)) {
			continue;
		}

		const options = this.getNodeParameter('options', i, {});
		const properties = { ...options };
		properties.title = sheetTitle;

		if (options.tabColor) {
			const { red, green, blue } = hexToRgb(options.tabColor as string)!;
			properties.tabColor = { red: red / 255, green: green / 255, blue: blue / 255 };
		}

		const requests = [
			{
				addSheet: {
					properties,
				},
			},
		];

		responseData = await apiRequest.call(
			this,
			'POST',
			`/v4/spreadsheets/${sheetName}:batchUpdate`,
			{ requests },
		);

		// simplify response
		Object.assign(responseData, responseData.replies[0].addSheet.properties);
		delete responseData.replies;

		existingSheetNames.push(sheetTitle);

		const executionData = this.helpers.constructExecutionMetaData(
			wrapData(responseData as IDataObject[]),
			{ itemData: { item: i } },
		);

		returnData.push(...executionData);
	}
	return returnData;
}
