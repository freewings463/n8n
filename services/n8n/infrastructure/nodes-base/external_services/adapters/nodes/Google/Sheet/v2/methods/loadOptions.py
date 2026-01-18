"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Sheet/v2/methods/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Sheet 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/GoogleSheet、../helpers/GoogleSheets.types、../helpers/GoogleSheets.utils。导出:无。关键函数/方法:getSheets、getSheetHeaderRow、getSheetHeaderRowAndAddColumn、getSheetHeaderRowWithGeneratedColumnNames、getSheetHeaderRowAndSkipEmpty。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Sheet/v2/methods/loadOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Sheet/v2/methods/loadOptions.py

import type { IDataObject, ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import { GoogleSheet } from '../helpers/GoogleSheet';
import type { ResourceLocator } from '../helpers/GoogleSheets.types';
import { getSpreadsheetId } from '../helpers/GoogleSheets.utils';

export async function getSheets(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const documentId = this.getNodeParameter('documentId', 0) as IDataObject | null;

	if (!documentId) return [];

	const { mode, value } = documentId;

	const spreadsheetId = getSpreadsheetId(this.getNode(), mode as ResourceLocator, value as string);

	const sheet = new GoogleSheet(spreadsheetId, this);
	const responseData = await sheet.spreadsheetGetSheets();

	if (responseData === undefined) {
		throw new NodeOperationError(this.getNode(), 'No data got returned');
	}

	const returnData: INodePropertyOptions[] = [];
	for (const entry of responseData.sheets!) {
		if (entry.properties!.sheetType !== 'GRID') {
			continue;
		}

		returnData.push({
			name: entry.properties!.title as string,
			value: entry.properties!.sheetId as unknown as string,
		});
	}

	return returnData;
}

export async function getSheetHeaderRow(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const documentId = this.getNodeParameter('documentId', 0) as IDataObject | null;

	if (!documentId) return [];

	const { mode, value } = documentId;

	const spreadsheetId = getSpreadsheetId(this.getNode(), mode as ResourceLocator, value as string);

	const sheet = new GoogleSheet(spreadsheetId, this);
	const sheetWithinDocument = this.getNodeParameter('sheetName', undefined, {
		extractValue: true,
	}) as string;
	const { mode: sheetMode } = this.getNodeParameter('sheetName', 0) as {
		mode: ResourceLocator;
	};

	const { title: sheetName } = await sheet.spreadsheetGetSheet(
		this.getNode(),
		sheetMode,
		sheetWithinDocument,
	);
	const sheetData = await sheet.getData(`${sheetName}!1:1`, 'FORMATTED_VALUE');

	if (sheetData === undefined) {
		throw new NodeOperationError(this.getNode(), 'No data got returned');
	}

	const columns = sheet.testFilter(sheetData, 0, 0);

	const returnData: INodePropertyOptions[] = [];

	for (const column of columns) {
		returnData.push({
			name: column as unknown as string,
			value: column as unknown as string,
		});
	}

	return returnData;
}

export async function getSheetHeaderRowAndAddColumn(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData = await getSheetHeaderRow.call(this);
	returnData.push({
		name: 'New column ...',
		value: 'newColumn',
	});
	const columnToMatchOn = this.getNodeParameter('columnToMatchOn', 0) as string;
	return returnData.filter((column) => column.value !== columnToMatchOn);
}

export async function getSheetHeaderRowWithGeneratedColumnNames(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData = await getSheetHeaderRow.call(this);
	return returnData.map((column, i) => {
		if (column.value !== '') return column;
		const indexBasedValue = `col_${i + 1}`;
		return {
			name: indexBasedValue,
			value: indexBasedValue,
		};
	});
}

export async function getSheetHeaderRowAndSkipEmpty(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData = await getSheetHeaderRow.call(this);
	return returnData.filter((column) => column.value);
}
