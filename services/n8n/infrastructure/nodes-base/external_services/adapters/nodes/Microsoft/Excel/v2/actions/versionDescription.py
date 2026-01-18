"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Excel/v2/actions/versionDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Excel 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./table/Table.resource、./workbook/Workbook.resource、./worksheet/Worksheet.resource。导出:versionDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-filename-against-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Excel/v2/actions/versionDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Excel/v2/actions/versionDescription.py

/* eslint-disable n8n-nodes-base/node-filename-against-convention */
import { NodeConnectionTypes, type INodeTypeDescription } from 'n8n-workflow';

import * as table from './table/Table.resource';
import * as workbook from './workbook/Workbook.resource';
import * as worksheet from './worksheet/Worksheet.resource';

export const versionDescription: INodeTypeDescription = {
	displayName: 'Microsoft Excel 365',
	name: 'microsoftExcel',
	icon: 'file:excel.svg',
	group: ['input'],
	version: [2, 2.1, 2.2],
	subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
	description: 'Consume Microsoft Excel API',
	defaults: {
		name: 'Microsoft Excel 365',
	},
	inputs: [NodeConnectionTypes.Main],
	outputs: [NodeConnectionTypes.Main],
	credentials: [
		{
			name: 'microsoftExcelOAuth2Api',
			required: true,
		},
	],
	properties: [
		{
			displayName:
				'This node connects to the Microsoft 365 cloud platform. Use the \'Extract from File\' and \'Convert to File\' nodes to directly manipulate spreadsheet files (.xls, .csv, etc). <a href="https://n8n.io/workflows/890-read-in-an-excel-spreadsheet-file/" target="_blank">More info</a>.',
			name: 'notice',
			type: 'notice',
			default: '',
		},
		{
			displayName: 'Resource',
			name: 'resource',
			type: 'options',
			noDataExpression: true,
			options: [
				{
					name: 'Table',
					value: 'table',
					description: 'Represents an Excel table',
				},
				{
					name: 'Workbook',
					value: 'workbook',
					description: 'A workbook is the top level object which contains one or more worksheets',
				},
				{
					name: 'Sheet',
					value: 'worksheet',
					description: 'A sheet is a grid of cells which can contain data, tables, charts, etc',
				},
			],
			default: 'workbook',
		},
		...table.description,
		...workbook.description,
		...worksheet.description,
	],
};
