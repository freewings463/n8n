"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Notion/shared/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Notion/shared 的节点。导入/依赖:外部:无；内部:无；本地:../GenericFunctions。导出:无。关键函数/方法:getDatabases。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Notion/shared/methods/listSearch.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Notion/shared/methods/listSearch.py

import type {
	IDataObject,
	ILoadOptionsFunctions,
	INodeListSearchItems,
	INodeListSearchResult,
} from 'n8n-workflow';

import { notionApiRequestAllItems } from '../GenericFunctions';

export async function getDatabases(
	this: ILoadOptionsFunctions,
	filter?: string,
): Promise<INodeListSearchResult> {
	const returnData: INodeListSearchItems[] = [];
	const body: IDataObject = {
		page_size: 100,
		query: filter,
		filter: { property: 'object', value: 'database' },
	};
	const databases = await notionApiRequestAllItems.call(this, 'results', 'POST', '/search', body);
	for (const database of databases) {
		returnData.push({
			name: database.title[0]?.plain_text || database.id,
			value: database.id,
			url: database.url,
		});
	}
	returnData.sort((a, b) => {
		if (a.name.toLocaleLowerCase() < b.name.toLocaleLowerCase()) {
			return -1;
		}
		if (a.name.toLocaleLowerCase() > b.name.toLocaleLowerCase()) {
			return 1;
		}
		return 0;
	});
	return { results: returnData };
}
