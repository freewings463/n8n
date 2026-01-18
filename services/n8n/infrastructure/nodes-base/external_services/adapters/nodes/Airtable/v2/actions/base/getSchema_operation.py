"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtable/v2/actions/base/getSchema.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtable/v2 的节点。导入/依赖:外部:无；内部:无；本地:../utils/utilities、../helpers/utils、../../transport、../common.descriptions 等1项。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtable/v2/actions/base/getSchema.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtable/v2/actions/base/getSchema_operation.py

import type {
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
	NodeApiError,
} from 'n8n-workflow';

import { updateDisplayOptions, wrapData } from '../../../../../utils/utilities';
import { processAirtableError } from '../../helpers/utils';
import { apiRequest } from '../../transport';
import { baseRLC } from '../common.descriptions';
import type { TablesResponse } from '../types';

const properties: INodeProperties[] = [
	{
		...baseRLC,
		description: 'The Airtable Base to retrieve the schema from',
	},
];

const displayOptions = {
	show: {
		resource: ['base'],
		operation: ['getSchema'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	items: INodeExecutionData[],
): Promise<INodeExecutionData[]> {
	let returnData: INodeExecutionData[] = [];

	for (let i = 0; i < items.length; i++) {
		try {
			const baseId = this.getNodeParameter('base', i, undefined, {
				extractValue: true,
			}) as string;

			const responseData: TablesResponse = await apiRequest.call(
				this,
				'GET',
				`meta/bases/${baseId}/tables`,
			);

			const executionData = this.helpers.constructExecutionMetaData(wrapData(responseData.tables), {
				itemData: { item: i },
			});

			returnData = returnData.concat(executionData);
		} catch (error) {
			error = processAirtableError(error as NodeApiError, undefined, i);
			if (this.continueOnFail()) {
				returnData.push({ json: { error: error.message } });
				continue;
			}
			throw error;
		}
	}

	return returnData;
}
