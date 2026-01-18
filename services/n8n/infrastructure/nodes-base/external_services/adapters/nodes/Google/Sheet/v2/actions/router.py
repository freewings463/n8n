"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Sheet/v2/actions/router.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Sheet 的路由。导入/依赖:外部:无；内部:n8n-workflow；本地:./sheet/Sheet.resource、./spreadsheet/SpreadSheet.resource、../helpers/GoogleSheet、../helpers/GoogleSheets.types 等1项。导出:无。关键函数/方法:router。用于组织该模块路由，绑定控制器与中间件，定义API边界。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Sheet/v2/actions/router.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Sheet/v2/actions/router.py

import { type IExecuteFunctions, type IDataObject, type INodeExecutionData } from 'n8n-workflow';

import * as sheet from './sheet/Sheet.resource';
import * as spreadsheet from './spreadsheet/SpreadSheet.resource';
import { GoogleSheet } from '../helpers/GoogleSheet';
import type { GoogleSheets, ResourceLocator } from '../helpers/GoogleSheets.types';
import { getSpreadsheetId } from '../helpers/GoogleSheets.utils';

export async function router(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
	let operationResult: INodeExecutionData[] = [];

	try {
		const resource = this.getNodeParameter('resource', 0);
		const operation = this.getNodeParameter('operation', 0);

		const googleSheets = {
			resource,
			operation,
		} as GoogleSheets;

		let results: INodeExecutionData[] | undefined;
		if (googleSheets.resource === 'sheet') {
			const { mode, value } = this.getNodeParameter('documentId', 0) as IDataObject;
			const spreadsheetId = getSpreadsheetId(
				this.getNode(),
				mode as ResourceLocator,
				value as string,
			);

			const googleSheet = new GoogleSheet(spreadsheetId, this);

			let sheetId = '';
			let sheetName = '';

			if (operation !== 'create') {
				const sheetWithinDocument = this.getNodeParameter('sheetName', 0, undefined, {
					extractValue: true,
				}) as string;
				const { mode: sheetMode } = this.getNodeParameter('sheetName', 0) as {
					mode: ResourceLocator;
				};

				const result = await googleSheet.spreadsheetGetSheet(
					this.getNode(),
					sheetMode,
					sheetWithinDocument,
				);
				sheetId = result.sheetId.toString();
				sheetName = result.title;
			}

			switch (operation) {
				case 'create':
					sheetName = spreadsheetId;
					break;
				case 'delete':
					sheetName = sheetId;
					break;
				case 'remove':
					sheetName = `${spreadsheetId}||${sheetId}`;
					break;
			}

			results = await sheet[googleSheets.operation].execute.call(
				this,
				googleSheet,
				sheetName,
				sheetId,
			);
		} else if (googleSheets.resource === 'spreadsheet') {
			results = await spreadsheet[googleSheets.operation].execute.call(this);
		}
		if (results?.length) {
			operationResult = operationResult.concat(results);
		}
	} catch (error) {
		if (this.continueOnFail()) {
			operationResult.push({ json: this.getInputData(0)[0].json, error });
		} else {
			throw error;
		}
	}

	return [operationResult];
}
