"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/SharePoint/descriptions/item/getAll.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/SharePoint 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/utils、../common.descriptions。导出:description。关键函数/方法:function。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/SharePoint/descriptions/item/getAll.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/SharePoint/descriptions/item/getAll_operation.py

import type { IExecuteSingleFunctions, IHttpRequestOptions, INodeProperties } from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import { itemGetAllFieldsPreSend } from '../../helpers/utils';
import { listRLC, siteRLC, untilSiteSelected } from '../common.descriptions';

const properties: INodeProperties[] = [
	{
		...siteRLC,
		description: 'Select the site to retrieve lists from',
	},
	{
		...listRLC,
		description: 'Select the list you want to search for items in',
		displayOptions: {
			hide: {
				...untilSiteSelected,
			},
		},
	},
	{
		displayName: 'Filter by Formula',
		name: 'filter',
		default: '',
		description:
			'The formula will be evaluated for each record. <a href="https://learn.microsoft.com/en-us/graph/filter-query-parameter">More info</a>.',
		hint: 'If empty, all the items will be returned',
		placeholder: "e.g. fields/Title eq 'item1'",
		routing: {
			send: {
				property: '$filter',
				type: 'query',
				value: '={{ $value ? $value : undefined }}',
			},
		},
		type: 'string',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		routing: {
			send: {
				paginate: '={{ $value }}',
			},
			operations: {
				pagination: {
					type: 'generic',
					properties: {
						continue: '={{ !!$response.body?.["@odata.nextLink"] }}',
						request: {
							url: '={{ $response.body?.["@odata.nextLink"] ?? $request.url }}',
							qs: {
								$select:
									'={{ !!$response.body?.["@odata.nextLink"] ? undefined : $request.qs?.$select }}',
							},
						},
					},
				},
			},
		},
		type: 'boolean',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		default: 50,
		description: 'Max number of results to return',
		displayOptions: {
			show: {
				returnAll: [false],
			},
		},
		routing: {
			send: {
				property: '$top',
				type: 'query',
				value: '={{ $value }}',
			},
		},
		type: 'number',
		typeOptions: {
			minValue: 1,
		},
		validateType: 'number',
	},
	{
		displayName: 'Options',
		name: 'options',
		default: {},
		options: [
			{
				displayName: 'Fields',
				name: 'fields',
				default: [],
				description: 'The fields you want to include in the output',
				displayOptions: {
					hide: {
						'/simplify': [true],
					},
				},
				options: [
					{
						name: 'Content Type',
						value: 'contentType',
					},
					{
						name: 'Created At',
						value: 'createdDateTime',
					},
					{
						name: 'Created By',
						value: 'createdBy',
					},
					{
						name: 'Fields',
						value: 'fields',
					},
					{
						name: 'ID',
						value: 'id',
					},
					{
						name: 'Last Modified At',
						value: 'lastModifiedDateTime',
					},
					{
						name: 'Last Modified By',
						value: 'lastModifiedBy',
					},

					{
						name: 'Parent Reference',
						value: 'parentReference',
					},
					{
						name: 'Web URL',
						value: 'webUrl',
					},
				],
				routing: {
					send: {
						preSend: [itemGetAllFieldsPreSend],
					},
				},
				type: 'multiOptions',
			},
		],
		placeholder: 'Add option',
		type: 'collection',
	},
	{
		displayName: 'Simplify',
		name: 'simplify',
		default: true,
		routing: {
			send: {
				preSend: [
					async function (
						this: IExecuteSingleFunctions,
						requestOptions: IHttpRequestOptions,
					): Promise<IHttpRequestOptions> {
						const simplify = this.getNodeParameter('simplify', false) as boolean;
						if (simplify) {
							requestOptions.qs ??= {};
							requestOptions.qs.$select = 'id,createdDateTime,lastModifiedDateTime,webUrl';
							requestOptions.qs.$expand = 'fields(select=Title)';
						}
						return requestOptions;
					},
				],
			},
		},
		type: 'boolean',
	},
];

const displayOptions = {
	show: {
		resource: ['item'],
		operation: ['getAll'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);
