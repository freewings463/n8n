"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/SharePoint/descriptions/item/get.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/SharePoint 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:description。关键函数/方法:function。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/SharePoint/descriptions/item/get.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/SharePoint/descriptions/item/get_operation.py

import type { IExecuteSingleFunctions, IHttpRequestOptions, INodeProperties } from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import {
	itemRLC,
	listRLC,
	siteRLC,
	untilListSelected,
	untilSiteSelected,
} from '../common.descriptions';

const properties: INodeProperties[] = [
	{
		...siteRLC,
		description: 'Select the site to retrieve lists from',
	},
	{
		...listRLC,
		description: 'Select the list you want to retrieve an item from',
		displayOptions: {
			hide: {
				...untilSiteSelected,
			},
		},
	},
	{
		...itemRLC,
		description: 'Select the item you want to get',
		displayOptions: {
			hide: {
				...untilSiteSelected,
				...untilListSelected,
			},
		},
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
		operation: ['get'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);
