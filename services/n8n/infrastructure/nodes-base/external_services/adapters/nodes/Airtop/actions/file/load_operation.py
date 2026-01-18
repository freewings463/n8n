"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/file/load.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./helpers。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/file/load.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/file/load_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import { pushFileToSession, triggerFileInput } from './helpers';
import {
	sessionIdField,
	windowIdField,
	elementDescriptionField,
	includeHiddenElementsField,
} from '../common/fields';

const displayOptions = {
	show: {
		resource: ['file'],
		operation: ['load'],
	},
};

export const description: INodeProperties[] = [
	{
		...sessionIdField,
		description: 'The session ID to load the file into',
		displayOptions,
	},
	{
		...windowIdField,
		description: 'The window ID to trigger the file input in',
		displayOptions,
	},
	{
		displayName: 'File ID',
		name: 'fileId',
		type: 'string',
		default: '',
		required: true,
		description: 'ID of the file to load into the session',
		displayOptions,
	},
	{
		...elementDescriptionField,
		description: 'Optional description of the file input to interact with',
		placeholder: 'e.g. the file upload selection box',
		displayOptions,
	},
	{
		...includeHiddenElementsField,
		displayOptions,
	},
];

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const fileId = this.getNodeParameter('fileId', index, '') as string;
	const sessionId = this.getNodeParameter('sessionId', index, '') as string;
	const windowId = this.getNodeParameter('windowId', index, '') as string;
	const elementDescription = this.getNodeParameter('elementDescription', index, '') as string;
	const includeHiddenElements = this.getNodeParameter(
		'includeHiddenElements',
		index,
		false,
	) as boolean;

	try {
		await pushFileToSession.call(this, fileId, sessionId);
		await triggerFileInput.call(this, {
			fileId,
			windowId,
			sessionId,
			elementDescription,
			includeHiddenElements,
		});

		return this.helpers.returnJsonArray({
			sessionId,
			windowId,
			data: {
				message: 'File loaded successfully',
			},
		});
	} catch (error) {
		throw new NodeOperationError(this.getNode(), error as Error);
	}
}
