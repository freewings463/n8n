"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/SpreadsheetFile/v2/toFile.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/SpreadsheetFile/v2 的节点。导入/依赖:外部:@utils/binary、@utils/utilities；内部:n8n-workflow；本地:../description。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/SpreadsheetFile/v2/toFile.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/SpreadsheetFile/v2/toFile_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';

import type { JsonToSpreadsheetBinaryFormat, JsonToSpreadsheetBinaryOptions } from '@utils/binary';
import { convertJsonToSpreadsheetBinary } from '@utils/binary';
import { generatePairedItemData } from '@utils/utilities';

import { toFileOptions, toFileProperties } from '../description';

export const description: INodeProperties[] = [...toFileProperties, toFileOptions];

export async function execute(this: IExecuteFunctions, items: INodeExecutionData[]) {
	const returnData: INodeExecutionData[] = [];

	const pairedItem = generatePairedItemData(items.length);

	try {
		const binaryPropertyName = this.getNodeParameter('binaryPropertyName', 0);
		const fileFormat = this.getNodeParameter('fileFormat', 0) as JsonToSpreadsheetBinaryFormat;
		const options = this.getNodeParameter('options', 0, {}) as JsonToSpreadsheetBinaryOptions;

		const binaryData = await convertJsonToSpreadsheetBinary.call(this, items, fileFormat, options);

		const newItem: INodeExecutionData = {
			json: {},
			binary: {
				[binaryPropertyName]: binaryData,
			},
			pairedItem,
		};

		returnData.push(newItem);
	} catch (error) {
		if (this.continueOnFail()) {
			returnData.push({
				json: {
					error: error.message,
				},
				pairedItem,
			});
		} else {
			throw error;
		}
	}
	return returnData;
}
