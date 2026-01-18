"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtable/v2/actions/record/upsert.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtable/v2 的节点。导入/依赖:外部:无；内部:无；本地:../utils/utilities、../helpers/interfaces、../helpers/utils、../../transport 等1项。导出:description。关键函数/方法:execute、wrapData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtable/v2/actions/record/upsert.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtable/v2/actions/record/upsert_operation.py

import type {
	IDataObject,
	INodeExecutionData,
	INodeProperties,
	IExecuteFunctions,
	NodeApiError,
} from 'n8n-workflow';

import { updateDisplayOptions, wrapData } from '../../../../../utils/utilities';
import type { UpdateRecord } from '../../helpers/interfaces';
import { processAirtableError, removeIgnored } from '../../helpers/utils';
import { apiRequest, apiRequestAllItems, batchUpdate } from '../../transport';
import { insertUpdateOptions } from '../common.descriptions';

const properties: INodeProperties[] = [
	{
		displayName: 'Columns',
		name: 'columns',
		type: 'resourceMapper',
		noDataExpression: true,
		default: {
			mappingMode: 'defineBelow',
			value: null,
		},
		required: true,
		typeOptions: {
			loadOptionsDependsOn: ['table.value', 'base.value'],
			resourceMapper: {
				resourceMapperMethod: 'getColumnsWithRecordId',
				mode: 'update',
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
		operation: ['upsert'],
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

	const columnsToMatchOn = this.getNodeParameter('columns.matchingColumns', 0) as string[];

	for (let i = 0; i < items.length; i++) {
		try {
			const records: UpdateRecord[] = [];
			const options = this.getNodeParameter('options', i, {});

			if (dataMode === 'autoMapInputData') {
				if (columnsToMatchOn.includes('id')) {
					const { id, ...fields } = items[i].json;

					records.push({
						id: id as string,
						fields: removeIgnored(fields, options.ignoreFields as string),
					});
				} else {
					records.push({ fields: removeIgnored(items[i].json, options.ignoreFields as string) });
				}
			}

			if (dataMode === 'defineBelow') {
				const fields = this.getNodeParameter('columns.value', i, []) as IDataObject;

				if (columnsToMatchOn.includes('id')) {
					const id = fields.id as string;
					delete fields.id;
					records.push({ id, fields });
				} else {
					records.push({ fields });
				}
			}

			const body: IDataObject = {
				typecast: options.typecast ? true : false,
			};

			if (!columnsToMatchOn.includes('id')) {
				body.performUpsert = { fieldsToMergeOn: columnsToMatchOn };
			}

			let responseData;
			try {
				responseData = await batchUpdate.call(this, endpoint, body, records);
			} catch (error) {
				if (error.httpCode === '422' && columnsToMatchOn.includes('id')) {
					const createBody = {
						...body,
						records: records.map(({ fields }) => ({ fields })),
					};
					responseData = await apiRequest.call(this, 'POST', endpoint, createBody);
				} else if (error?.description?.includes('Cannot update more than one record')) {
					const conditions = columnsToMatchOn
						.map((column) => `{${column}} = '${records[0].fields[column]}'`)
						.join(',');
					const response = await apiRequestAllItems.call(
						this,
						'GET',
						endpoint,
						{},
						{
							fields: columnsToMatchOn,
							filterByFormula: `AND(${conditions})`,
						},
					);
					const matches = response.records as UpdateRecord[];

					const updateRecords: UpdateRecord[] = [];

					if (options.updateAllMatches) {
						updateRecords.push(...matches.map(({ id }) => ({ id, fields: records[0].fields })));
					} else {
						updateRecords.push({ id: matches[0].id, fields: records[0].fields });
					}

					responseData = await batchUpdate.call(this, endpoint, body, updateRecords);
				} else {
					throw error;
				}
			}

			const executionData = this.helpers.constructExecutionMetaData(
				wrapData(responseData.records as IDataObject[]),
				{ itemData: { item: i } },
			);

			returnData.push(...executionData);
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
