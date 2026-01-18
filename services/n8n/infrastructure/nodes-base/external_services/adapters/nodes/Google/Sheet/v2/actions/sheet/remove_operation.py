"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Sheet/v2/actions/sheet/remove.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Sheet 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../utils/utilities、../helpers/GoogleSheet、../../transport。导出:无。关键函数/方法:execute、wrapData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Sheet/v2/actions/sheet/remove.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Sheet/v2/actions/sheet/remove_operation.py

import type { IExecuteFunctions, IDataObject, INodeExecutionData } from 'n8n-workflow';

import { wrapData } from '../../../../../../utils/utilities';
import type { GoogleSheet } from '../../helpers/GoogleSheet';
import { apiRequest } from '../../transport';

export async function execute(
	this: IExecuteFunctions,
	_sheet: GoogleSheet,
	sheetName: string,
): Promise<INodeExecutionData[]> {
	const returnData: INodeExecutionData[] = [];
	const items = this.getInputData();
	for (let i = 0; i < items.length; i++) {
		const [spreadsheetId, sheetWithinDocument] = sheetName.split('||');
		const requests = [
			{
				deleteSheet: {
					sheetId: sheetWithinDocument,
				},
			},
		];

		const responseData = await apiRequest.call(
			this,
			'POST',
			`/v4/spreadsheets/${spreadsheetId}:batchUpdate`,
			{ requests },
		);
		delete responseData.replies;

		const executionData = this.helpers.constructExecutionMetaData(
			wrapData(responseData as IDataObject[]),
			{ itemData: { item: i } },
		);

		returnData.push(...executionData);
	}

	return returnData;
}
