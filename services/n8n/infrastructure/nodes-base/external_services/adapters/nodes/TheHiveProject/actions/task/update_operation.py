"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/task/update.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的节点。导入/依赖:外部:lodash/set、@utils/utilities；内部:n8n-workflow；本地:../helpers/utils、../../transport。导出:description。关键函数/方法:execute、set、matches、wrapData。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/task/update.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/task/update_operation.py

import set from 'lodash/set';
import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import { updateDisplayOptions, wrapData } from '@utils/utilities';

import { fixFieldType, prepareInputItem } from '../../helpers/utils';
import { theHiveApiRequest } from '../../transport';

const properties: INodeProperties[] = [
	{
		displayName: 'Fields',
		name: 'taskUpdateFields',
		type: 'resourceMapper',
		default: {
			mappingMode: 'defineBelow',
			value: null,
		},
		noDataExpression: true,
		required: true,
		typeOptions: {
			resourceMapper: {
				resourceMapperMethod: 'getTaskUpdateFields',
				mode: 'update',
				valuesLabel: 'Fields',
				addAllFields: true,
				multiKeyMatch: true,
			},
		},
	},
];

const displayOptions = {
	show: {
		resource: ['task'],
		operation: ['update'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	i: number,
	item: INodeExecutionData,
): Promise<INodeExecutionData[]> {
	let body: IDataObject = {};
	let updated = 1;

	const dataMode = this.getNodeParameter('taskUpdateFields.mappingMode', i) as string;

	if (dataMode === 'autoMapInputData') {
		const schema = this.getNodeParameter('taskUpdateFields.schema', i) as IDataObject[];
		body = prepareInputItem(item.json, schema, i);
	}

	if (dataMode === 'defineBelow') {
		const taskUpdateFields = this.getNodeParameter('taskUpdateFields.value', i, []) as IDataObject;
		body = taskUpdateFields;
	}

	body = fixFieldType(body);

	const fieldsToMatchOn = this.getNodeParameter('taskUpdateFields.matchingColumns', i) as string[];

	const updateBody: IDataObject = {};
	const matchFields: IDataObject = {};
	const { id } = body; // id would be used if matching on id, also we need to remove it from the body

	for (const field of Object.keys(body)) {
		if (fieldsToMatchOn.includes(field)) {
			// if field is in fieldsToMatchOn, we need to exclude it from the updateBody, as values used for matching should not be updated
			matchFields[field] = body[field];
		} else {
			// use set to construct the updateBody, as it allows to process customFields.fieldName
			// if customFields provided under customFields property, it will be send as is
			set(updateBody, field, body[field]);
		}
	}

	if (fieldsToMatchOn.includes('id')) {
		await theHiveApiRequest.call(this, 'PATCH', `/v1/task/${id}`, body);
	} else {
		const filter = {
			_name: 'filter',
			_and: fieldsToMatchOn.map((field) => ({
				_eq: {
					_field: field,
					_value: matchFields[field],
				},
			})),
		};

		const queryBody = {
			query: [
				{
					_name: 'listTask',
				},
				filter,
			],
		};

		const matches = (await theHiveApiRequest.call(
			this,
			'POST',
			'/v1/query',
			queryBody,
		)) as IDataObject[];

		if (!matches.length) {
			throw new NodeOperationError(this.getNode(), 'No matching alerts found');
		}
		const ids = matches.map((match) => match._id);
		updated = ids.length;

		updateBody.ids = ids;

		await theHiveApiRequest.call(this, 'PATCH', '/v1/task/_bulk', updateBody);
	}

	const executionData = this.helpers.constructExecutionMetaData(
		wrapData({ success: true, updated }),
		{
			itemData: { item: i },
		},
	);

	return executionData;
}
