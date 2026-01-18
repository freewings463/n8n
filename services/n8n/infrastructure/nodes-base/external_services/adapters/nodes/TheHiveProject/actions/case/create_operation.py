"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/case/create.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的节点。导入/依赖:外部:lodash/set、@utils/utilities；内部:无；本地:../helpers/utils、../../transport。导出:description。关键函数/方法:execute、set。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/case/create.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/case/create_operation.py

import set from 'lodash/set';
import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { updateDisplayOptions, wrapData } from '@utils/utilities';

import { fixFieldType, prepareInputItem } from '../../helpers/utils';
import { theHiveApiRequest } from '../../transport';

const properties: INodeProperties[] = [
	{
		displayName: 'Fields',
		name: 'caseFields',
		type: 'resourceMapper',
		default: {
			mappingMode: 'defineBelow',
			value: null,
		},
		noDataExpression: true,
		required: true,
		typeOptions: {
			resourceMapper: {
				resourceMapperMethod: 'getCaseFields',
				mode: 'add',
				valuesLabel: 'Fields',
			},
		},
	},
];

const displayOptions = {
	show: {
		resource: ['case'],
		operation: ['create'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(
	this: IExecuteFunctions,
	i: number,
	item: INodeExecutionData,
): Promise<INodeExecutionData[]> {
	let responseData: IDataObject | IDataObject[] = [];
	let inputData: IDataObject = {};

	const dataMode = this.getNodeParameter('caseFields.mappingMode', i) as string;

	if (dataMode === 'autoMapInputData') {
		const schema = this.getNodeParameter('caseFields.schema', i) as IDataObject[];
		inputData = prepareInputItem(item.json, schema, i);
	}

	if (dataMode === 'defineBelow') {
		const caseFields = this.getNodeParameter('caseFields.value', i, []) as IDataObject;
		inputData = caseFields;
	}

	inputData = fixFieldType(inputData);

	const body: IDataObject = {};

	for (const field of Object.keys(inputData)) {
		// use set to construct the updateBody, as it allows to process customFields.fieldName
		// if customFields provided under customFields property, it will be send as is
		set(body, field, inputData[field]);
	}

	responseData = await theHiveApiRequest.call(this, 'POST', '/v1/case' as string, body);

	const executionData = this.helpers.constructExecutionMetaData(wrapData(responseData), {
		itemData: { item: i },
	});

	return executionData;
}
