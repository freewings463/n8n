"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Analytics/v2/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Analytics 的节点。导入/依赖:外部:无；内部:无；本地:../helpers/utils、../transport。导出:无。关键函数/方法:searchProperties、searchViews。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Analytics/v2/methods/listSearch.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Analytics/v2/methods/listSearch.py

import type {
	ILoadOptionsFunctions,
	INodeListSearchItems,
	INodeListSearchResult,
} from 'n8n-workflow';

import { sortLoadOptions } from '../helpers/utils';
import { googleApiRequest } from '../transport';

export async function searchProperties(
	this: ILoadOptionsFunctions,
): Promise<INodeListSearchResult> {
	const returnData: INodeListSearchItems[] = [];

	const { accounts } = await googleApiRequest.call(
		this,
		'GET',
		'',
		{},
		{},
		'https://analyticsadmin.googleapis.com/v1alpha/accounts',
	);

	for (const acount of accounts || []) {
		const { properties } = await googleApiRequest.call(
			this,
			'GET',
			'',
			{},
			{ filter: `parent:${acount.name}` },
			'https://analyticsadmin.googleapis.com/v1alpha/properties',
		);

		if (properties && properties.length > 0) {
			for (const property of properties) {
				const name = property.displayName;
				const value = property.name.split('/')[1] || property.name;
				const url = `https://analytics.google.com/analytics/web/#/p${value}/`;
				returnData.push({ name, value, url });
			}
		}
	}
	return {
		results: sortLoadOptions(returnData),
	};
}

export async function searchViews(this: ILoadOptionsFunctions): Promise<INodeListSearchResult> {
	const returnData: INodeListSearchItems[] = [];
	const { items } = await googleApiRequest.call(
		this,
		'GET',
		'',
		{},
		{},
		'https://www.googleapis.com/analytics/v3/management/accounts/~all/webproperties/~all/profiles',
	);

	for (const item of items) {
		returnData.push({
			name: `${item.name} [${item.websiteUrl}]`,
			value: item.id,
			url: `https://analytics.google.com/analytics/web/#/report-home/a${item.accountId}w${item.internalWebPropertyId}p${item.id}`,
		});
	}

	return {
		results: sortLoadOptions(returnData),
	};
}
