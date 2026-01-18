"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Excel/v2/methods/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Excel 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../transport、../helpers/utils。导出:无。关键函数/方法:getWorksheetColumnRow、getWorksheetColumnRowSkipColumnToMatchOn、getTableColumns。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Excel/v2/methods/loadOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Excel/v2/methods/loadOptions.py

import type { IDataObject, ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';

import { microsoftApiRequest } from '../transport';
import { parseAddress } from '../helpers/utils';

export async function getWorksheetColumnRow(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const workbookId = this.getNodeParameter('workbook', undefined, {
		extractValue: true,
	}) as string;

	const worksheetId = this.getNodeParameter('worksheet', undefined, {
		extractValue: true,
	}) as string;

	let range = this.getNodeParameter('range', '') as string;
	let columns: string[] = [];

	if (range === '') {
		const worksheetData = await microsoftApiRequest.call(
			this,
			'GET',
			`/drive/items/${workbookId}/workbook/worksheets/${worksheetId}/usedRange`,
			undefined,
			{ select: 'values' },
		);

		columns = worksheetData.values[0] as string[];
	} else {
		const { cellFrom, cellTo } = parseAddress(range);

		range = `${cellFrom.value}:${cellTo.column}${cellFrom.row}`;
		const worksheetData = await microsoftApiRequest.call(
			this,
			'PATCH',
			`/drive/items/${workbookId}/workbook/worksheets/${worksheetId}/range(address='${range}')`,
			{ select: 'values' },
		);

		columns = worksheetData.values[0] as string[];
	}

	const returnData: INodePropertyOptions[] = [];
	for (const column of columns) {
		returnData.push({
			name: column,
			value: column,
		});
	}
	return returnData;
}

export async function getWorksheetColumnRowSkipColumnToMatchOn(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData = await getWorksheetColumnRow.call(this);
	const columnToMatchOn = this.getNodeParameter('columnToMatchOn', 0) as string;
	return returnData.filter((column) => column.value !== columnToMatchOn);
}

export async function getTableColumns(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const workbookId = this.getNodeParameter('workbook', undefined, {
		extractValue: true,
	}) as string;

	const worksheetId = this.getNodeParameter('worksheet', undefined, {
		extractValue: true,
	}) as string;

	const tableId = this.getNodeParameter('table', undefined, {
		extractValue: true,
	}) as string;

	const response = await microsoftApiRequest.call(
		this,
		'GET',
		`/drive/items/${workbookId}/workbook/worksheets/${worksheetId}/tables/${tableId}/columns`,
		{},
	);

	return (response.value as IDataObject[]).map((column) => ({
		name: column.name as string,
		value: column.name as string,
	}));
}
