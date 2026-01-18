"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/AzureCosmosDb/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/AzureCosmosDb 的节点。导入/依赖:外部:无；内部:无；本地:../helpers/constants、../transport。导出:无。关键函数/方法:formatResults、searchContainers、responseData、searchItems。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/AzureCosmosDb/methods/listSearch.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/AzureCosmosDb/methods/listSearch.py

import type {
	IDataObject,
	ILoadOptionsFunctions,
	INodeListSearchResult,
	INodeListSearchItems,
} from 'n8n-workflow';

import { HeaderConstants } from '../helpers/constants';
import { azureCosmosDbApiRequest } from '../transport';

function formatResults(items: IDataObject[], filter?: string): INodeListSearchItems[] {
	return items
		.map(({ id }) => ({
			name: String(id).replace(/ /g, ''),
			value: String(id),
		}))
		.filter(({ name }) => !filter || name.includes(filter))
		.sort((a, b) => a.name.localeCompare(b.name));
}

export async function searchContainers(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const headers = paginationToken ? { [HeaderConstants.X_MS_CONTINUATION]: paginationToken } : {};
	const responseData = (await azureCosmosDbApiRequest.call(
		this,
		'GET',
		'/colls',
		{},
		{},
		headers,
		true,
	)) as {
		body: IDataObject;
		headers: IDataObject;
	};

	const containers = responseData.body.DocumentCollections as IDataObject[];

	return {
		results: formatResults(containers, filter),
		paginationToken: responseData.headers[HeaderConstants.X_MS_CONTINUATION],
	};
}

export async function searchItems(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const container = this.getCurrentNodeParameter('container', {
		extractValue: true,
	}) as string;
	const headers = paginationToken ? { [HeaderConstants.X_MS_CONTINUATION]: paginationToken } : {};
	const responseData = (await azureCosmosDbApiRequest.call(
		this,
		'GET',
		`/colls/${container}/docs`,
		{},
		{},
		headers,
		true,
	)) as {
		body: IDataObject;
		headers: IDataObject;
	};

	const items = responseData.body.Documents as IDataObject[];

	return {
		results: formatResults(items, filter),
		paginationToken: responseData.headers[HeaderConstants.X_MS_CONTINUATION],
	};
}
