"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtable/v2/actions/record/create.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtable/v2 的节点。导入/依赖:外部:无；内部:无；本地:../utils/utilities、../helpers/utils、../../transport、../common.descriptions。导出:description。关键函数/方法:execute、wrapData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtable/v2/actions/record/create.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtable/v2/actions/record/create_operation.py

import type {
	IDataObject,
	INodeExecutionData,
	INodeProperties,
	IExecuteFunctions,
	NodeApiError,
} from 'n8n-workflow';

import { updateDisplayOptions, wrapData } from '../../../../../utils/utilities';
import { processAirtableError, removeIgnored } from '../../helpers/utils';
import { apiRequest } from '../../transport';
import { insertUpdateOptions } from '../common.descriptions';

const properties: INodeProperties[] = [
	{
		displayName: 'Columns',
		name: 'columns',
		type: 'resourceMapper',
		default: {
			mappingMode: 'defineBelow',
			value: null,
		},
		noDataExpression: true,
		required: true,
		typeOptions: {
			loadOptionsDependsOn: ['table.value', 'base.value'],
			resourceMapper: {
				resourceMapperMethod: 'getColumns',
				mode: 'add',
				fieldWords: {
					singular: 'column',
					plural: 'columns',
				},
				addAllFields: true,
				multiKeyMatch: true,
			},
		},
	},
	...insertUpdateOptions,
];

const displayOptions = {
	show: {
		resource: ['record'],
		operation: ['create'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	items: INodeExecutionData[],
	base: string,
	table: string,
): Promise<INodeExecutionData[]> {
	const returnData: INodeExecutionData[] = [];

	const endpoint = `${base}/${table}`;

	const dataMode = this.getNodeParameter('columns.mappingMode', 0) as string;

	for (let i = 0; i < items.length; i++) {
		try {
			const options = this.getNodeParameter('options', i, {});
			const typecast = Boolean(options.typecast);

			const body: IDataObject = { typecast };

			if (dataMode === 'autoMapInputData') {
				body.fields = removeIgnored(items[i].json, options.ignoreFields as string);
			}

			if (dataMode === 'defineBelow') {
				const fields = this.getNodeParameter('columns.value', i, [], {
					skipValidation: typecast,
				}) as IDataObject;

				body.fields = fields;
			}

			const responseData = await apiRequest.call(this, 'POST', endpoint, body);

			const executionData = this.helpers.constructExecutionMetaData(
				wrapData(responseData as IDataObject[]),
				{ itemData: { item: i } },
			);

			returnData.push.apply(returnData, executionData);
		} catch (error) {
			error = processAirtableError(error as NodeApiError, undefined, i);
			if (this.continueOnFail()) {
				returnData.push({ json: { message: error.message, error } });
				continue;
			}
			throw error;
		}
	}

	return returnData;
}
