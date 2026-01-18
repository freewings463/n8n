"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/messageAttachment/download.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的节点。导入/依赖:外部:@utils/utilities；内部:n8n-workflow；本地:../../descriptions、../../transport。导出:properties、description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/v2/actions/messageAttachment/download.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/v2/actions/messageAttachment/download_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';

import { updateDisplayOptions } from '@utils/utilities';

import { attachmentRLC, messageRLC } from '../../descriptions';
import { microsoftApiRequest } from '../../transport';

export const properties: INodeProperties[] = [
	messageRLC,
	attachmentRLC,
	{
		displayName: 'Put Output in Field',
		name: 'binaryPropertyName',
		hint: 'The name of the output field to put the binary file data in',
		type: 'string',
		required: true,
		default: 'data',
	},
];

const displayOptions = {
	show: {
		resource: ['messageAttachment'],
		operation: ['download'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, index: number, items: INodeExecutionData[]) {
	const messageId = this.getNodeParameter('messageId', index, undefined, {
		extractValue: true,
	}) as string;

	const attachmentId = this.getNodeParameter('attachmentId', index, undefined, {
		extractValue: true,
	}) as string;

	const dataPropertyNameDownload = this.getNodeParameter('binaryPropertyName', index);

	// Get attachment details first
	const attachmentDetails = await microsoftApiRequest.call(
		this,
		'GET',
		`/messages/${messageId}/attachments/${attachmentId}`,
		undefined,
		{ $select: 'id,name,contentType' },
	);

	let mimeType: string | undefined;
	if (attachmentDetails.contentType) {
		mimeType = attachmentDetails.contentType;
	}
	const fileName = attachmentDetails.name as string;

	const response = await microsoftApiRequest.call(
		this,
		'GET',
		`/messages/${messageId}/attachments/${attachmentId}/$value`,
		undefined,
		{},
		undefined,
		{},
		{ encoding: null, resolveWithFullResponse: true },
	);

	const newItem: INodeExecutionData = {
		json: items[index].json,
		binary: {},
	};

	if (items[index].binary !== undefined) {
		// Create a shallow copy of the binary data so that the old
		// data references which do not get changed still stay behind
		// but the incoming data does not get changed.
		Object.assign(newItem.binary!, items[index].binary);
	}

	const data = Buffer.from(response.body as string, 'utf8');
	newItem.binary![dataPropertyNameDownload] = await this.helpers.prepareBinaryData(
		data,
		fileName,
		mimeType,
	);

	const executionData = this.helpers.constructExecutionMetaData(
		this.helpers.returnJsonArray(newItem),
		{ itemData: { item: index } },
	);

	return executionData;
}
