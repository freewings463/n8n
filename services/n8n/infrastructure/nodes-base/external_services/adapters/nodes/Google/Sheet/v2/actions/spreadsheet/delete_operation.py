"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Sheet/v2/actions/spreadsheet/delete.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Sheet 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../utils/utilities、../../constants、../helpers/GoogleSheets.types、../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Sheet/v2/actions/spreadsheet/delete.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Sheet/v2/actions/spreadsheet/delete_operation.py

import type { IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';

import { wrapData } from '../../../../../../utils/utilities';
import { GOOGLE_DRIVE_FILE_URL_REGEX } from '../../../../constants';
import type { SpreadSheetProperties } from '../../helpers/GoogleSheets.types';
import { apiRequest } from '../../transport';

export const description: SpreadSheetProperties = [
	{
		displayName: 'Document',
		name: 'documentId',
		type: 'resourceLocator',
		default: { mode: 'list', value: '' },
		required: true,
		modes: [
			{
				displayName: 'From List',
				name: 'list',
				type: 'list',
				typeOptions: {
					searchListMethod: 'spreadSheetsSearch',
					searchable: true,
				},
			},
			{
				displayName: 'By URL',
				name: 'url',
				type: 'string',
				extractValue: {
					type: 'regex',
					regex: GOOGLE_DRIVE_FILE_URL_REGEX,
				},
				validation: [
					{
						type: 'regex',
						properties: {
							regex: GOOGLE_DRIVE_FILE_URL_REGEX,
							errorMessage: 'Not a valid Google Drive File URL',
						},
					},
				],
			},
			{
				displayName: 'By ID',
				name: 'id',
				type: 'string',
				validation: [
					{
						type: 'regex',
						properties: {
							regex: '[a-zA-Z0-9\\-_]{2,}',
							errorMessage: 'Not a valid Google Drive File ID',
						},
					},
				],
				url: '=https://docs.google.com/spreadsheets/d/{{$value}}/edit',
			},
		],
		displayOptions: {
			show: {
				resource: ['spreadsheet'],
				operation: ['deleteSpreadsheet'],
			},
		},
	},
];

export async function execute(this: IExecuteFunctions): Promise<INodeExecutionData[]> {
	const items = this.getInputData();
	const returnData: INodeExecutionData[] = [];

	for (let i = 0; i < items.length; i++) {
		const documentId = this.getNodeParameter('documentId', i, undefined, {
			extractValue: true,
		}) as string;

		await apiRequest.call(
			this,
			'DELETE',
			'',
			{},
			{},
			`https://www.googleapis.com/drive/v3/files/${documentId}`,
		);

		const executionData = this.helpers.constructExecutionMetaData(wrapData({ success: true }), {
			itemData: { item: i },
		});

		returnData.push(...executionData);
	}

	return returnData;
}
