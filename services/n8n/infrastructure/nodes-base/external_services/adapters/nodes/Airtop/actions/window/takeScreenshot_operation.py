"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/window/takeScreenshot.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:无；本地:../../transport。导出:description。关键函数/方法:execute、validateAirtopApiResponse。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/window/takeScreenshot.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/window/takeScreenshot_operation.py

import type {
	IExecuteFunctions,
	INodeExecutionData,
	IBinaryData,
	INodeProperties,
} from 'n8n-workflow';

import {
	validateSessionAndWindowId,
	validateAirtopApiResponse,
	convertScreenshotToBinary,
} from '../../GenericFunctions';
import { apiRequest } from '../../transport';

export const description: INodeProperties[] = [
	{
		displayName: 'Output Binary Image',
		description: 'Whether to output the image as a binary file instead of a base64 encoded string',
		name: 'outputImageAsBinary',
		type: 'boolean',
		default: false,
		displayOptions: {
			show: {
				resource: ['window'],
				operation: ['takeScreenshot'],
			},
		},
	},
];

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const { sessionId, windowId } = validateSessionAndWindowId.call(this, index);
	const outputImageAsBinary = this.getNodeParameter('outputImageAsBinary', index, false) as boolean;

	let data: IBinaryData | undefined; // for storing the binary data
	let image = ''; // for storing the base64 encoded image

	const response = await apiRequest.call(
		this,
		'POST',
		`/sessions/${sessionId}/windows/${windowId}/screenshot`,
	);

	// validate response
	validateAirtopApiResponse(this.getNode(), response);

	// process screenshot on success
	if (response.meta?.screenshots?.length) {
		if (outputImageAsBinary) {
			const buffer = convertScreenshotToBinary(response.meta.screenshots[0]);
			data = await this.helpers.prepareBinaryData(buffer, 'screenshot.jpg', 'image/jpeg');
		} else {
			image = response?.meta?.screenshots?.[0].dataUrl;
		}
	}

	return [
		{
			json: {
				sessionId,
				windowId,
				image,
			},
			...(data ? { binary: { data } } : {}),
		},
	];
}
