"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Excel/v2/actions/table/convertToRange.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Excel 的节点。导入/依赖:外部:@utils/utilities；内部:无；本地:../../transport、../common.descriptions。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Excel/v2/actions/table/convertToRange.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Excel/v2/actions/table/convertToRange_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import { microsoftApiRequest } from '../../transport';
import { tableRLC, workbookRLC, worksheetRLC } from '../common.descriptions';

const properties: INodeProperties[] = [workbookRLC, worksheetRLC, tableRLC];

const displayOptions = {
	show: {
		resource: ['table'],
		operation: ['convertToRange'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	items: INodeExecutionData[],
): Promise<INodeExecutionData[]> {
	const returnData: INodeExecutionData[] = [];

	for (let i = 0; i < items.length; i++) {
		try {
			const workbookId = this.getNodeParameter('workbook', i, undefined, {
				extractValue: true,
			}) as string;

			const worksheetId = this.getNodeParameter('worksheet', i, undefined, {
				extractValue: true,
			}) as string;

			const tableId = this.getNodeParameter('table', i, undefined, {
				extractValue: true,
			}) as string;

			const responseData = await microsoftApiRequest.call(
				this,
				'POST',
				`/drive/items/${workbookId}/workbook/worksheets/${worksheetId}/tables/${tableId}/convertToRange`,
			);

			const executionData = this.helpers.constructExecutionMetaData(
				this.helpers.returnJsonArray(responseData as IDataObject),
				{ itemData: { item: i } },
			);

			returnData.push(...executionData);
		} catch (error) {
			if (this.continueOnFail()) {
				const executionErrorData = this.helpers.constructExecutionMetaData(
					this.helpers.returnJsonArray({ error: error.message }),
					{ itemData: { item: i } },
				);
				returnData.push(...executionErrorData);
				continue;
			}
			throw error;
		}
	}

	return returnData;
}
