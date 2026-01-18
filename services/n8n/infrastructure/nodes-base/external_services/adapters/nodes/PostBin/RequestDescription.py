"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/PostBin/RequestDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/PostBin 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:requestOperations、requestFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/PostBin/RequestDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/PostBin/RequestDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { buildBinTestURL, buildRequestURL } from './GenericFunctions';

// Operations for the `Request` resource
export const requestOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['request'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get a request',
				routing: {
					request: {
						method: 'GET',
						url: '=/api/bin/{{$parameter["binId"]}}/req/{{$parameter["requestId"]}}',
					},
					send: {
						preSend: [
							// Parse binId before sending to make sure it's in the right format
							buildRequestURL,
						],
					},
				},
				action: 'Get a request',
			},
			{
				name: 'Remove First',
				value: 'removeFirst',
				description: 'Remove the first request from bin',
				routing: {
					request: {
						method: 'GET',
						url: '=/api/bin/{{$parameter["binId"]}}/req/shift',
					},
					send: {
						preSend: [
							// Parse binId before sending to make sure it's in the right format
							buildRequestURL,
						],
					},
				},
				action: 'Remove First a request',
			},
			{
				name: 'Send',
				value: 'send',
				description: 'Send a test request to the bin',
				routing: {
					request: {
						method: 'POST',
					},
					send: {
						preSend: [
							// Parse binId before sending to make sure it's in the right format
							buildBinTestURL,
						],
					},
					output: {
						postReceive: [
							{
								type: 'set',
								properties: {
									value: '={{ { "requestId": $response.body } }}',
								},
							},
						],
					},
				},
				action: 'Send a request',
			},
		],
		default: 'get',
	},
];

// Properties of the `Request` resource
export const requestFields: INodeProperties[] = [
	{
		displayName: 'Bin ID',
		name: 'binId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['request'],
				operation: ['get', 'removeFirst', 'send'],
			},
		},
		description: 'Unique identifier for each bin',
	},
	{
		displayName: 'Bin Content',
		name: 'binContent',
		type: 'string',
		default: '',
		typeOptions: {
			rows: 5,
		},
		displayOptions: {
			show: {
				resource: ['request'],
				operation: ['send'],
			},
		},
		// Content is sent in the body of POST requests
		routing: {
			send: {
				property: 'content',
				type: 'body',
			},
		},
	},
	{
		displayName: 'Request ID',
		name: 'requestId',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: {
				resource: ['request'],
				operation: ['get'],
			},
		},
		description: 'Unique identifier for each request',
	},
];
