"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/v2/methods/loadOptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../transport。导出:无。关键函数/方法:getCategoriesNames、getFolders、getCalendarGroups。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/v2/methods/loadOptions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/v2/methods/loadOptions.py

import type { ILoadOptionsFunctions, INodePropertyOptions } from 'n8n-workflow';

import { getSubfolders, microsoftApiRequestAllItems } from '../transport';

export async function getCategoriesNames(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const categories = await microsoftApiRequestAllItems.call(
		this,
		'value',
		'GET',
		'/outlook/masterCategories',
	);
	for (const category of categories) {
		returnData.push({
			name: category.displayName as string,
			value: category.displayName as string,
		});
	}
	return returnData;
}

export async function getFolders(this: ILoadOptionsFunctions): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const response = await microsoftApiRequestAllItems.call(this, 'value', 'GET', '/mailFolders', {});
	const folders = await getSubfolders.call(this, response);
	for (const folder of folders) {
		returnData.push({
			name: folder.displayName as string,
			value: folder.id as string,
		});
	}
	return returnData;
}

export async function getCalendarGroups(
	this: ILoadOptionsFunctions,
): Promise<INodePropertyOptions[]> {
	const returnData: INodePropertyOptions[] = [];
	const calendars = await microsoftApiRequestAllItems.call(
		this,
		'value',
		'GET',
		'/calendarGroups',
		{},
	);
	for (const calendar of calendars) {
		returnData.push({
			name: calendar.name as string,
			value: calendar.id as string,
		});
	}
	return returnData;
}
