"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/interaction/type.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:无；本地:./helpers、../../transport、../common/fields。导出:description。关键函数/方法:execute、validateAirtopApiResponse。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/interaction/type.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/interaction/type_operation.py

import {
	type IExecuteFunctions,
	type INodeExecutionData,
	type INodeProperties,
} from 'n8n-workflow';

import { constructInteractionRequest } from './helpers';
import {
	validateRequiredStringField,
	validateSessionAndWindowId,
	validateAirtopApiResponse,
} from '../../GenericFunctions';
import { apiRequest } from '../../transport';
import { elementDescriptionField } from '../common/fields';

export const description: INodeProperties[] = [
	{
		displayName: 'Text',
		name: 'text',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['interaction'],
				operation: ['type'],
			},
		},
		description: 'The text to type into the browser window',
		placeholder: 'e.g. email@example.com',
	},
	{
		displayName: 'Press Enter Key',
		name: 'pressEnterKey',
		type: 'boolean',
		default: false,
		description: 'Whether to press the Enter key after typing the text',
		displayOptions: {
			show: {
				resource: ['interaction'],
				operation: ['type'],
			},
		},
	},
	{
		...elementDescriptionField,
		displayOptions: {
			show: {
				resource: ['interaction'],
				operation: ['type'],
			},
		},
	},
];

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const { sessionId, windowId } = validateSessionAndWindowId.call(this, index);
	const text = validateRequiredStringField.call(this, index, 'text', 'Text');
	const pressEnterKey = this.getNodeParameter('pressEnterKey', index) as boolean;
	const elementDescription = this.getNodeParameter('elementDescription', index) as string;

	const request = constructInteractionRequest.call(this, index, {
		text,
		pressEnterKey,
		elementDescription,
	});

	const response = await apiRequest.call(
		this,
		'POST',
		`/sessions/${sessionId}/windows/${windowId}/type`,
		request,
	);

	validateAirtopApiResponse(this.getNode(), response);

	return this.helpers.returnJsonArray({ sessionId, windowId, ...response });
}
