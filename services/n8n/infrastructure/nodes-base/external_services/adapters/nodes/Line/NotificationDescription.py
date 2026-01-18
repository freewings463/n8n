"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Line/NotificationDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Line 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:notificationOperations、notificationFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Line/NotificationDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Line/NotificationDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const notificationOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['notification'],
			},
		},
		options: [
			{
				name: 'Send',
				value: 'send',
				description: 'Sends notifications to users or groups',
				action: 'Send a notification',
			},
		],
		default: 'send',
	},
];

export const notificationFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 notification:send                          */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Message',
		name: 'message',
		required: true,
		type: 'string',
		displayOptions: {
			show: {
				operation: ['send'],
				resource: ['notification'],
			},
		},
		default: '',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				operation: ['send'],
				resource: ['notification'],
			},
		},
		options: [
			{
				displayName: 'Image',
				name: 'imageUi',
				placeholder: 'Add Image',
				type: 'fixedCollection',
				typeOptions: {
					multipleValues: false,
				},
				default: {},
				options: [
					{
						name: 'imageValue',
						displayName: 'Image',
						values: [
							{
								displayName: 'Binary File',
								name: 'binaryData',
								type: 'boolean',
								default: false,
							},
							{
								displayName: 'Image Full Size',
								name: 'imageFullsize',
								type: 'string',
								default: '',
								displayOptions: {
									show: {
										binaryData: [false],
									},
								},
								description: 'HTTP/HTTPS URL. Maximum size of 2048×2048px JPEG.',
							},
							{
								displayName: 'Image Thumbnail',
								name: 'imageThumbnail',
								type: 'string',
								displayOptions: {
									show: {
										binaryData: [false],
									},
								},
								default: '',
								description: 'HTTP/HTTPS URL. Maximum size of 240×240px JPEG.',
							},
							{
								displayName: 'Input Binary Field',
								name: 'binaryProperty',
								type: 'string',
								displayOptions: {
									show: {
										binaryData: [true],
									},
								},
								default: 'data',
								hint: 'The name of the input binary field containing the file to be written',
							},
						],
					},
				],
			},
			{
				displayName: 'Notification Disabled',
				name: 'notificationDisabled',
				type: 'boolean',
				default: false,
				// eslint-disable-next-line n8n-nodes-base/node-param-description-boolean-without-whether
				description:
					"<p>true: The user doesn't receive a push notification when the message is sent.</p><p>false: The user receives a push notification when the message is sent</p>",
			},
			{
				displayName: 'Sticker',
				name: 'stickerUi',
				placeholder: 'Add Sticker',
				type: 'fixedCollection',
				typeOptions: {
					multipleValues: false,
				},
				default: {},
				options: [
					{
						name: 'stickerValue',
						displayName: 'Sticker',
						values: [
							{
								displayName: 'Sticker ID',
								name: 'stickerId',
								type: 'number',
								default: '',
							},
							{
								displayName: 'Sticker Package ID',
								name: 'stickerPackageId',
								type: 'number',
								default: '',
								description: 'Package ID',
							},
						],
					},
				],
			},
		],
	},
];
