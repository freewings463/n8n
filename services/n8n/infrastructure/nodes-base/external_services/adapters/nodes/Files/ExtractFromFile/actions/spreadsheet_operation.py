"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Files/ExtractFromFile/actions/spreadsheet.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Files/ExtractFromFile 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../v2/fromFile.operation。导出:operations、description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Files/ExtractFromFile/actions/spreadsheet.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Files/ExtractFromFile/actions/spreadsheet_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';

import * as fromFile from '../../../SpreadsheetFile/v2/fromFile.operation';

export const operations = ['csv', 'html', 'rtf', 'ods', 'xls', 'xlsx'];

export const description: INodeProperties[] = fromFile.description
	.filter((property) => property.name !== 'fileFormat')
	.map((property) => {
		const newProperty = { ...property };
		newProperty.displayOptions = {
			show: {
				operation: operations,
			},
		};

		if (newProperty.name === 'options') {
			newProperty.options = (newProperty.options as INodeProperties[]).map((option) => {
				let newOption = option;
				if (
					[
						'delimiter',
						'encoding',
						'fromLine',
						'maxRowCount',
						'enableBOM',
						'relaxQuotes',
						'skipRecordsWithErrors',
					].includes(option.name)
				) {
					newOption = { ...option, displayOptions: { show: { '/operation': ['csv'] } } };
				}
				if (option.name === 'sheetName') {
					newOption = {
						...option,
						displayOptions: { show: { '/operation': ['ods', 'xls', 'xlsx'] } },
						description: 'Name of the sheet to read from in the spreadsheet',
					};
				}
				if (option.name === 'range') {
					newOption = {
						...option,
						displayOptions: { show: { '/operation': ['ods', 'xls', 'xlsx'] } },
					};
				}
				if (['includeEmptyCells', 'headerRow'].includes(option.name)) {
					newOption = {
						...option,
						displayOptions: { show: { '/operation': ['ods', 'xls', 'xlsx', 'csv', 'html'] } },
					};
				}
				return newOption;
			});
		}
		return newProperty;
	});

export async function execute(
	this: IExecuteFunctions,
	items: INodeExecutionData[],
	fileFormatProperty: string,
	options?: fromFile.FromFileOptions,
) {
	const returnData: INodeExecutionData[] = await fromFile.execute.call(
		this,
		items,
		fileFormatProperty,
		options,
	);
	return returnData;
}
