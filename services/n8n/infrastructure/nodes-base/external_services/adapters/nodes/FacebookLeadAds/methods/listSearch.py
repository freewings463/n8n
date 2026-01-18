"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/FacebookLeadAds/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/FacebookLeadAds/methods 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../GenericFunctions。导出:无。关键函数/方法:filterMatches、pageList、formList。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/FacebookLeadAds/methods/listSearch.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/FacebookLeadAds/methods/listSearch.py

import type { ILoadOptionsFunctions, INodeListSearchResult } from 'n8n-workflow';

import { facebookFormList, facebookPageList } from '../GenericFunctions';

const filterMatches = (name: string, filter?: string): boolean =>
	!filter || name?.toLowerCase().includes(filter.toLowerCase());

export async function pageList(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const { data: pages, paging } = await facebookPageList.call(this, paginationToken);
	return {
		results: pages
			.filter((page) => filterMatches(page.name, filter))
			.map((page) => ({
				name: page.name,
				value: page.id,
				url: `https://facebook.com/${page.id}`,
			})),
		paginationToken: paging?.next ? paging?.cursors?.after : undefined,
	};
}

export async function formList(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const pageId = this.getNodeParameter('page', '', { extractValue: true }) as string;

	const { data: forms, paging } = await facebookFormList.call(this, pageId, paginationToken);
	return {
		results: forms
			.filter((form) => filterMatches(form.name, filter))
			.map((form) => ({
				name: form.name,
				value: form.id,
			})),
		paginationToken: paging?.next ? paging?.cursors?.after : undefined,
	};
}
