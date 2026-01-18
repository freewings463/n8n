"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/case/addAttachment.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/TheHiveProject/actions 的节点。导入/依赖:外部:@utils/utilities；内部:无；本地:../../descriptions、../../transport。导出:description。关键函数/方法:execute、inputDataFields。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/case/addAttachment.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/case/addAttachment_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { updateDisplayOptions, wrapData } from '@utils/utilities';

import { attachmentsUi, caseRLC } from '../../descriptions';
import { theHiveApiRequest } from '../../transport';

const properties: INodeProperties[] = [
	caseRLC,
	attachmentsUi,
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		options: [
			{
				displayName: 'Rename Files',
				name: 'canRename',
				type: 'boolean',
				description: 'Whether to rename the file in case a file with the same name already exists',
				default: false,
			},
		],
	},
];

const displayOptions = {
	show: {
		resource: ['case'],
		operation: ['addAttachment'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	let responseData: IDataObject | IDataObject[] = [];

	const caseId = this.getNodeParameter('caseId', i, '', { extractValue: true }) as string;
	const canRename = this.getNodeParameter('options.canRename', i, false) as boolean;

	const inputDataFields = (
		this.getNodeParameter('attachmentsUi.values', i, []) as IDataObject[]
	).map((entry) => (entry.field as string).trim());

	const attachments = [];

	for (const inputDataField of inputDataFields) {
		const binaryData = this.helpers.assertBinaryData(i, inputDataField);
		const dataBuffer = await this.helpers.getBinaryDataBuffer(i, inputDataField);

		attachments.push({
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
		`/v1/case/${caseId}/attachments`,
		undefined,
		undefined,
		undefined,
		{
			Headers: {
				'Content-Type': 'multipart/form-data',
			},
			formData: {
				attachments,
				canRename: JSON.stringify(canRename),
			},
		},
	);

	const executionData = this.helpers.constructExecutionMetaData(wrapData(responseData), {
		itemData: { item: i },
	});

	return executionData;
}
