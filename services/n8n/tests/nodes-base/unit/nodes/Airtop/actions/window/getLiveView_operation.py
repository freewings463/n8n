"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/window/getLiveView.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../constants、../../GenericFunctions、../../transport。导出:description。关键函数/方法:execute、screenResolution、validateAirtopApiResponse。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected test/non-production code -> tests/*
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/window/getLiveView.operation.ts -> services/n8n/tests/nodes-base/unit/nodes/Airtop/actions/window/getLiveView_operation.py

import type { IExecuteFunctions, INodeExecutionData, INodeProperties } from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import { ERROR_MESSAGES } from '../../constants';
import { validateAirtopApiResponse, validateSessionAndWindowId } from '../../GenericFunctions';
import { apiRequest } from '../../transport';

export const description: INodeProperties[] = [
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['window'],
				operation: ['getLiveView'],
			},
		},
		options: [
			{
				displayName: 'Include Navigation Bar',
				name: 'includeNavigationBar',
				type: 'boolean',
				default: false,
				description:
					'Whether to include the navigation bar in the Live View. When enabled, the navigation bar will be visible allowing you to navigate between pages.',
			},
			{
				displayName: 'Screen Resolution',
				name: 'screenResolution',
				type: 'string',
				default: '',
				description:
					'The screen resolution of the Live View. Setting a resolution will force the window to open at that specific size.',
				placeholder: 'e.g. 1280x720',
			},
			{
				displayName: 'Disable Resize',
				name: 'disableResize',
				type: 'boolean',
				default: false,
				description: 'Whether to disable the window from being resized in the Live View',
			},
		],
	},
];

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const { sessionId, windowId } = validateSessionAndWindowId.call(this, index);
	const additionalFields = this.getNodeParameter('additionalFields', index);

	const queryParams: Record<string, any> = {};

	if (additionalFields.includeNavigationBar) {
		queryParams.includeNavigationBar = true;
	}

	if (additionalFields.screenResolution) {
		const screenResolution = ((additionalFields.screenResolution as string) || '')
			.trim()
			.toLowerCase();
		const regex = /^\d{3,4}x\d{3,4}$/; // Expected format: 1280x720

		if (!regex.test(screenResolution)) {
			throw new NodeOperationError(this.getNode(), ERROR_MESSAGES.SCREEN_RESOLUTION_INVALID, {
				itemIndex: index,
			});
		}

		queryParams.screenResolution = screenResolution;
	}

	if (additionalFields.disableResize) {
		queryParams.disableResize = true;
	}

	const response = await apiRequest.call(
		this,
		'GET',
		`/sessions/${sessionId}/windows/${windowId}`,
		undefined,
		queryParams,
	);

	validateAirtopApiResponse(this.getNode(), response);

	return this.helpers.returnJsonArray({ sessionId, windowId, ...response });
}
