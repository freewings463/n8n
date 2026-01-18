"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/log/create.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的节点。导入/依赖:外部:@utils/utilities；内部:无；本地:../../descriptions、../helpers/utils、../../transport。导出:description。关键函数/方法:execute、inputDataFields。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/log/create.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/log/create_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { updateDisplayOptions, wrapData } from '@utils/utilities';

import { attachmentsUi, taskRLC } from '../../descriptions';
import { fixFieldType, prepareInputItem } from '../../helpers/utils';
import { theHiveApiRequest } from '../../transport';

const properties: INodeProperties[] = [
	taskRLC,
	{
		displayName: 'Fields',
		name: 'logFields',
		type: 'resourceMapper',
		default: {
			mappingMode: 'defineBelow',
			value: null,
		},
		noDataExpression: true,
		required: true,
		typeOptions: {
			resourceMapper: {
				resourceMapperMethod: 'getLogFields',
				mode: 'add',
				valuesLabel: 'Fields',
			},
		},
	},
	attachmentsUi,
];

const displayOptions = {
	show: {
		resource: ['log'],
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
	let body: IDataObject = {};

	const dataMode = this.getNodeParameter('logFields.mappingMode', i) as string;
	const taskId = this.getNodeParameter('taskId', i, '', { extractValue: true }) as string;

	if (dataMode === 'autoMapInputData') {
		const schema = this.getNodeParameter('logFields.schema', i) as IDataObject[];
		body = prepareInputItem(item.json, schema, i);
	}

	if (dataMode === 'defineBelow') {
		const logFields = this.getNodeParameter('logFields.value', i, []) as IDataObject;
		body = logFields;
	}

	body = fixFieldType(body);

	const inputDataFields = (
		this.getNodeParameter('attachmentsUi.values', i, []) as IDataObject[]
	).map((entry) => (entry.field as string).trim());

	if (inputDataFields.length) {
		const binaries = [];

		for (const inputDataField of inputDataFields) {
			const binaryData = this.helpers.assertBinaryData(i, inputDataField);
			const dataBuffer = await this.helpers.getBinaryDataBuffer(i, inputDataField);

			binaries.push({
				value: dataBuffer,
				options: {
					contentType: binaryData.mimeType,
					filename: binaryData.fileName,
				},
			});
		}

		responseData = await theHiveApiRequest.call(
			this,
			'POST',
			`/v1/task/${taskId}/log`,
			undefined,
			undefined,
			undefined,
			{
				Headers: {
					'Content-Type': 'multipart/form-data',
				},
				formData: {
					attachments: binaries,
					_json: JSON.stringify(body),
				},
			},
		);
	} else {
		responseData = await theHiveApiRequest.call(this, 'POST', `/v1/task/${taskId}/log`, body);
	}

	const executionData = this.helpers.constructExecutionMetaData(wrapData(responseData), {
		itemData: { item: i },
	});

	return executionData;
}
