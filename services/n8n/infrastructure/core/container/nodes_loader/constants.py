"""
MIGRATION-META:
  source_path: packages/core/src/nodes-loader/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/core/src/nodes-loader 的模块。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:CUSTOM_NODES_CATEGORY、CUSTOM_NODES_PACKAGE_NAME、commonPollingParameters、commonCORSParameters、commonDeclarativeNodeOptionParameters。关键函数/方法:无。用于承载该模块实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node loading/discovery -> infrastructure/container/nodes_loader
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/core/src/nodes-loader/constants.ts -> services/n8n/infrastructure/core/container/nodes_loader/constants.py

import type { INodeProperties } from 'n8n-workflow';
import { cronNodeOptions } from 'n8n-workflow';

export const CUSTOM_NODES_CATEGORY = 'Custom Nodes';
export const CUSTOM_NODES_PACKAGE_NAME = 'CUSTOM';

export const commonPollingParameters: INodeProperties[] = [
	{
		displayName: 'Poll Times',
		name: 'pollTimes',
		type: 'fixedCollection',
		typeOptions: {
			multipleValues: true,
			multipleValueButtonText: 'Add Poll Time',
		},
		default: { item: [{ mode: 'everyMinute' }] },
		description: 'Time at which polling should occur',
		placeholder: 'Add Poll Time',
		options: cronNodeOptions,
	},
];

export const commonCORSParameters: INodeProperties[] = [
	{
		displayName: 'Allowed Origins (CORS)',
		name: 'allowedOrigins',
		type: 'string',
		default: '*',
		description:
			'Comma-separated list of URLs allowed for cross-origin non-preflight requests. Use * (default) to allow all origins.',
	},
];

export const commonDeclarativeNodeOptionParameters: INodeProperties = {
	displayName: 'Request Options',
	name: 'requestOptions',
	type: 'collection',
	isNodeSetting: true,
	placeholder: 'Add Option',
	default: {},
	options: [
		{
			displayName: 'Batching',
			name: 'batching',
			placeholder: 'Add Batching',
			type: 'fixedCollection',
			typeOptions: {
				multipleValues: false,
			},
			default: {
				batch: {},
			},
			options: [
				{
					displayName: 'Batching',
					name: 'batch',
					values: [
						{
							displayName: 'Items per Batch',
							name: 'batchSize',
							type: 'number',
							typeOptions: {
								minValue: -1,
							},
							default: 50,
							description:
								'Input will be split in batches to throttle requests. -1 for disabled. 0 will be treated as 1.',
						},
						{
							displayName: 'Batch Interval (ms)',
							name: 'batchInterval',
							type: 'number',
							typeOptions: {
								minValue: 0,
							},
							default: 1000,
							description: 'Time (in milliseconds) between each batch of requests. 0 for disabled.',
						},
					],
				},
			],
		},
		{
			displayName: 'Ignore SSL Issues (Insecure)',
			name: 'allowUnauthorizedCerts',
			type: 'boolean',
			noDataExpression: true,
			default: false,
			description:
				'Whether to accept the response even if SSL certificate validation is not possible',
		},
		{
			displayName: 'Proxy',
			name: 'proxy',
			type: 'string',
			default: '',
			placeholder: 'e.g. http://myproxy:3128',
			description:
				'HTTP proxy to use. If authentication is required it can be defined as follow: http://username:password@myproxy:3128',
		},
		{
			displayName: 'Timeout',
			name: 'timeout',
			type: 'number',
			typeOptions: {
				minValue: 1,
			},
			default: 10000,
			description:
				'Time in ms to wait for the server to send response headers (and start the response body) before aborting the request',
		},
	],
};
