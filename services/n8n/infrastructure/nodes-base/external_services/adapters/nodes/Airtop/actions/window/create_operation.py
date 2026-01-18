"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/window/create.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport、../transport/types、../common/fields。导出:description。关键函数/方法:execute、validateAirtopApiResponse。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/window/create.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/window/create_operation.py

import type {
	IExecuteFunctions,
	INodeExecutionData,
	IDataObject,
	INodeProperties,
} from 'n8n-workflow';
import { NodeApiError } from 'n8n-workflow';

import {
	validateAirtopApiResponse,
	validateSessionId,
	validateUrl,
	validateScreenResolution,
} from '../../GenericFunctions';
import { apiRequest } from '../../transport';
import type { IAirtopResponse } from '../../transport/types';
import { urlField } from '../common/fields';

export const description: INodeProperties[] = [
	{
		...urlField,
		description: 'Initial URL to load in the window. Defaults to https://www.google.com.',
		displayOptions: {
			show: {
				resource: ['window'],
				operation: ['create'],
			},
		},
	},
	// Live View Options
	{
		displayName: 'Get Live View',
		name: 'getLiveView',
		type: 'boolean',
		default: false,
		description:
			'Whether to get the URL of the window\'s <a href="https://docs.airtop.ai/guides/how-to/creating-a-live-view" target="_blank">Live View</a>',
		displayOptions: {
			show: {
				resource: ['window'],
				operation: ['create'],
			},
		},
	},
	{
		displayName: 'Include Navigation Bar',
		name: 'includeNavigationBar',
		type: 'boolean',
		default: false,
		description:
			'Whether to include the navigation bar in the Live View. When enabled, the navigation bar will be visible allowing you to navigate between pages.',
		displayOptions: {
			show: {
				resource: ['window'],
				operation: ['create'],
				getLiveView: [true],
			},
		},
	},
	{
		displayName: 'Screen Resolution',
		name: 'screenResolution',
		type: 'string',
		default: '',
		description:
			'The screen resolution of the Live View. Setting a resolution will force the window to open at that specific size.',
		placeholder: 'e.g. 1280x720',
		displayOptions: {
			show: {
				resource: ['window'],
				operation: ['create'],
				getLiveView: [true],
			},
		},
	},
	{
		displayName: 'Disable Resize',
		name: 'disableResize',
		type: 'boolean',
		default: false,
		description: 'Whether to disable the window from being resized in the Live View',
		displayOptions: {
			show: {
				resource: ['window'],
				operation: ['create'],
				getLiveView: [true],
			},
		},
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['window'],
				operation: ['create'],
			},
		},
		options: [
			{
				displayName: 'Wait Until',
				name: 'waitUntil',
				type: 'options',
				description: 'Wait until the specified loading event occurs',
				default: 'load',
				options: [
					{
						name: 'Load',
						value: 'load',
						description: 'Wait until the page dom and its assets have loaded',
					},
					{
						name: 'DOM Content Loaded',
						value: 'domContentLoaded',
						description: 'Wait until the page DOM has loaded',
					},
					{
						name: 'Complete',
						value: 'complete',
						description: 'Wait until all iframes in the page have loaded',
					},
					{
						name: 'No Wait',
						value: 'noWait',
						description: 'Do not wait for any loading event and it will return immediately',
					},
				],
			},
		],
	},
];

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const sessionId = validateSessionId.call(this, index);
	const url = validateUrl.call(this, index);
	const additionalFields = this.getNodeParameter('additionalFields', index);
	// Live View Options
	const getLiveView = this.getNodeParameter('getLiveView', index, false);
	const includeNavigationBar = this.getNodeParameter('includeNavigationBar', index, false);
	const screenResolution = validateScreenResolution.call(this, index);
	const disableResize = this.getNodeParameter('disableResize', index, false);

	let response: IAirtopResponse;

	const body: IDataObject = {
		url,
		...additionalFields,
	};

	response = await apiRequest.call(this, 'POST', `/sessions/${sessionId}/windows`, body);

	if (!response?.data?.windowId) {
		throw new NodeApiError(this.getNode(), {
			message: 'Failed to create window',
			code: 500,
		});
	}

	const windowId = String(response.data.windowId);

	if (getLiveView) {
		// Get Window info
		response = await apiRequest.call(
			this,
			'GET',
			`/sessions/${sessionId}/windows/${windowId}`,
			undefined,
			{
				...(includeNavigationBar && { includeNavigationBar: true }),
				...(screenResolution && { screenResolution }),
				...(disableResize && { disableResize: true }),
			},
		);
	}

	// validate response
	validateAirtopApiResponse(this.getNode(), response);

	return this.helpers.returnJsonArray({ sessionId, windowId, ...response });
}
