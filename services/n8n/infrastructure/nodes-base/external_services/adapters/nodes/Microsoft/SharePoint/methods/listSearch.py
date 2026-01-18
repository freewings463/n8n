"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/SharePoint/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/SharePoint 的节点。导入/依赖:外部:无；内部:无；本地:../helpers/interfaces、../helpers/utils、../transport。导出:无。关键函数/方法:getFiles、getFolders、getItems、getLists、getSites。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/SharePoint/methods/listSearch.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/SharePoint/methods/listSearch.py

import type {
	IDataObject,
	ILoadOptionsFunctions,
	INodeListSearchItems,
	INodeListSearchResult,
} from 'n8n-workflow';

import type { IDriveItem, IList, IListItem, ISite } from '../helpers/interfaces';
import { escapeFilterValue } from '../helpers/utils';
import { microsoftSharePointApiRequest } from '../transport';

export async function getFiles(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const site = this.getNodeParameter('site', undefined, { extractValue: true }) as string;
	const folder = this.getNodeParameter('folder', undefined, { extractValue: true }) as string;

	let response: any;
	if (paginationToken) {
		response = await microsoftSharePointApiRequest.call(
			this,
			'GET',
			`/sites/${site}/drive/items/${folder}/children`,
			{},
			undefined,
			undefined,
			paginationToken,
		);
	} else {
		// File filter not supported
		// https://learn.microsoft.com/en-us/onedrive/developer/rest-api/concepts/filtering-results?view=odsp-graph-online#filterable-properties
		const qs: IDataObject = {
			$select: 'id,name,file',
		};
		if (filter) {
			qs.$filter = `startswith(name, '${escapeFilterValue(filter)}')`;
		}
		response = await microsoftSharePointApiRequest.call(
			this,
			'GET',
			`/sites/${site}/drive/items/${folder}/children`,
			{},
			qs,
		);
	}

	const items: IDriveItem[] = response.value;

	const results: INodeListSearchItems[] = items
		.filter((x) => x.file)
		.map((g) => ({
			name: g.name,
			value: g.id,
		}))
		.sort((a, b) =>
			a.name.localeCompare(b.name, undefined, { numeric: true, sensitivity: 'base' }),
		);

	return { results, paginationToken: response['@odata.nextLink'] };
}

export async function getFolders(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const site = this.getNodeParameter('site', undefined, { extractValue: true }) as string;

	let response: any;
	if (paginationToken) {
		response = await microsoftSharePointApiRequest.call(
			this,
			'GET',
			`/sites/${site}/drive/items`,
			{},
			undefined,
			undefined,
			paginationToken,
		);
	} else {
		const qs: IDataObject = {
			$select: 'id,name,folder',
			// Folder filter not supported, but filter is still required
			// https://learn.microsoft.com/en-us/onedrive/developer/rest-api/concepts/filtering-results?view=odsp-graph-online#filterable-properties
			$filter: 'folder ne null',
		};
		response = await microsoftSharePointApiRequest.call(
			this,
			'GET',
			`/sites/${site}/drive/items`,
			{},
			qs,
		);
	}

	const items: IDriveItem[] = response.value;

	const results: INodeListSearchItems[] = items
		.filter((x) => x.folder && (!filter || x.name?.toLowerCase()?.includes?.(filter.toLowerCase())))
		.map((g) => ({
			name: g.name,
			value: g.id,
		}))
		.sort((a, b) =>
			a.name.localeCompare(b.name, undefined, { numeric: true, sensitivity: 'base' }),
		);

	return { results, paginationToken: response['@odata.nextLink'] };
}

export async function getItems(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const site = this.getNodeParameter('site', undefined, { extractValue: true }) as string;
	const list = this.getNodeParameter('list', undefined, { extractValue: true }) as string;

	let response: any;
	if (paginationToken) {
		response = await microsoftSharePointApiRequest.call(
			this,
			'GET',
			`/sites/${site}/lists/${list}/items`,
			{},
			undefined,
			undefined,
			paginationToken,
		);
	} else {
		const qs: IDataObject = {
			$expand: 'fields(select=Title)',
			$select: 'id,fields',
		};
		if (filter) {
			qs.$filter = `fields/Title eq '${escapeFilterValue(filter)}'`;
		}
		response = await microsoftSharePointApiRequest.call(
			this,
			'GET',
			`/sites/${site}/lists/${list}/items`,
			{},
			qs,
		);
	}

	const items: IListItem[] = response.value;

	const results: INodeListSearchItems[] = items
		.map((g) => ({
			name: g.fields.Title ?? g.id,
			value: g.id,
		}))
		.sort((a, b) =>
			a.name.localeCompare(b.name, undefined, { numeric: true, sensitivity: 'base' }),
		);

	return { results, paginationToken: response['@odata.nextLink'] };
}

export async function getLists(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const site = this.getNodeParameter('site', undefined, { extractValue: true }) as string;

	let response: any;
	if (paginationToken) {
		response = await microsoftSharePointApiRequest.call(
			this,
			'GET',
			`/sites/${site}/lists`,
			{},
			undefined,
			undefined,
			paginationToken,
		);
	} else {
		const qs: IDataObject = {
			$select: 'id,displayName',
		};
		if (filter) {
			qs.$filter = `displayName eq '${escapeFilterValue(filter)}'`;
		}
		response = await microsoftSharePointApiRequest.call(
			this,
			'GET',
			`/sites/${site}/lists`,
			{},
			qs,
		);
	}

	const lists: IList[] = response.value;

	const results: INodeListSearchItems[] = lists
		.map((g) => ({
			name: g.displayName,
			value: g.id,
		}))
		.sort((a, b) =>
			a.name.localeCompare(b.name, undefined, { numeric: true, sensitivity: 'base' }),
		);

	return { results, paginationToken: response['@odata.nextLink'] };
}

export async function getSites(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	let response: any;
	if (paginationToken) {
		response = await microsoftSharePointApiRequest.call(
			this,
			'GET',
			'/sites',
			{},
			undefined,
			undefined,
			paginationToken,
		);
	} else {
		const qs: IDataObject = {
			$select: 'id,title',
			$search: '*',
		};
		if (filter) {
			qs.$search = filter;
		}
		response = await microsoftSharePointApiRequest.call(this, 'GET', '/sites', {}, qs);
	}

	const sites: ISite[] = response.value;

	const results: INodeListSearchItems[] = sites
		.map((g) => ({
			name: g.title,
			value: g.id,
		}))
		.sort((a, b) =>
			a.name.localeCompare(b.name, undefined, { numeric: true, sensitivity: 'base' }),
		);

	return { results, paginationToken: response['@odata.nextLink'] };
}
