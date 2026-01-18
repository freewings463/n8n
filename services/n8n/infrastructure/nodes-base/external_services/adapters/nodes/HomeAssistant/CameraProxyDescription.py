"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/HomeAssistant/CameraProxyDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/HomeAssistant 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:cameraProxyOperations、cameraProxyFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/HomeAssistant/CameraProxyDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/HomeAssistant/CameraProxyDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const cameraProxyOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['cameraProxy'],
			},
		},
		options: [
			{
				name: 'Get Screenshot',
				value: 'getScreenshot',
				description: 'Get the camera screenshot',
				action: 'Get a screenshot',
			},
		],
		default: 'getScreenshot',
	},
];

export const cameraProxyFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                       cameraProxy:getScreenshot                            */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Camera Entity Name or ID',
		name: 'cameraEntityId',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		typeOptions: {
			loadOptionsMethod: 'getCameraEntities',
		},
		default: '',
		required: true,
		displayOptions: {
			show: {
				operation: ['getScreenshot'],
				resource: ['cameraProxy'],
			},
		},
	},
	{
		displayName: 'Put Output File in Field',
		name: 'binaryPropertyName',
		type: 'string',
		required: true,
		default: 'data',
		displayOptions: {
			show: {
				operation: ['getScreenshot'],
				resource: ['cameraProxy'],
			},
		},
		hint: 'The name of the output binary field to put the file in',
	},
];
