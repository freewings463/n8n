"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Npm/DistTagDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Npm 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:distTagOperations、distTagFields。关键函数/方法:function。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Npm/DistTagDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Npm/DistTagDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const distTagOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		default: 'getMany',
		displayOptions: {
			show: {
				resource: ['distTag'],
			},
		},

		options: [
			{
				name: 'Get All',
				value: 'getMany',
				action: 'Returns all the dist-tags for a package',
				description: 'Returns all the dist-tags for a package',
				routing: {
					request: {
						method: 'GET',
						url: '=/-/package/{{ encodeURIComponent($parameter.packageName) }}/dist-tags',
					},
				},
			},
			{
				name: 'Update',
				value: 'update',
				action: 'Update a the dist-tags for a package',
				description: 'Update a the dist-tags for a package',
				routing: {
					request: {
						method: 'PUT',
						url: '=/-/package/{{ encodeURIComponent($parameter.packageName) }}/dist-tags/{{ encodeURIComponent($parameter.distTagName) }}',
					},
					send: {
						preSend: [
							async function (this, requestOptions) {
								requestOptions.headers!['content-type'] = 'application/x-www-form-urlencoded';
								requestOptions.body = this.getNodeParameter('packageVersion');
								return requestOptions;
							},
						],
					},
				},
			},
		],
	},
];

export const distTagFields: INodeProperties[] = [
	{
		displayName: 'Package Name',
		name: 'packageName',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['distTag'],
				operation: ['getMany', 'update'],
			},
		},
	},
	{
		displayName: 'Package Version',
		name: 'packageVersion',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['distTag'],
				operation: ['update'],
			},
		},
	},
	{
		displayName: 'Distribution Tag Name',
		name: 'distTagName',
		type: 'string',
		required: true,
		default: 'latest',
		displayOptions: {
			show: {
				resource: ['distTag'],
				operation: ['update'],
			},
		},
	},
];
