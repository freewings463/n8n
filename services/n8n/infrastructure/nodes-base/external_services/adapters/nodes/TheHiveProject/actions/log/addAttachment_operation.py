"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/TheHiveProject/actions/log/addAttachment.operation.ts
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
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/TheHiveProject/actions/log/addAttachment.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/TheHiveProject/actions/log/addAttachment_operation.py

import type {
	IDataObject,
	IExecuteFunctions,
	INodeExecutionData,
	INodeProperties,
} from 'n8n-workflow';

import { updateDisplayOptions, wrapData } from '@utils/utilities';

import { attachmentsUi, logRLC } from '../../descriptions';
import { theHiveApiRequest } from '../../transport';

const properties: INodeProperties[] = [logRLC, attachmentsUi];

const displayOptions = {
	show: {
		resource: ['log'],
		operation: ['addAttachment'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const logId = this.getNodeParameter('logId', i, '', { extractValue: true }) as string;

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

	await theHiveApiRequest.call(
		this,
		'POST',
		`/v1/log/${logId}/attachments`,
		undefined,
		undefined,
		undefined,
		{
			Headers: {
				'Content-Type': 'multipart/form-data',
			},
			formData: {
				attachments,
			},
		},
	);

	const executionData = this.helpers.constructExecutionMetaData(wrapData({ success: true }), {
		itemData: { item: i },
	});

	return executionData;
}
