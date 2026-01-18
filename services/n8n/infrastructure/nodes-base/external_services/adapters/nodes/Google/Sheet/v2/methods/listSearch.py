"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Sheet/v2/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Sheet 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/GoogleSheets.types、../helpers/GoogleSheets.utils、../transport。导出:无。关键函数/方法:spreadSheetsSearch、sheetsSearch。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Sheet/v2/methods/listSearch.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Sheet/v2/methods/listSearch.py

import type {
	IDataObject,
	ILoadOptionsFunctions,
	INodeListSearchItems,
	INodeListSearchResult,
} from 'n8n-workflow';
import { NodeOperationError } from 'n8n-workflow';

import type { ResourceLocator } from '../helpers/GoogleSheets.types';
import { getSpreadsheetId } from '../helpers/GoogleSheets.utils';
import { apiRequest } from '../transport';

export async function spreadSheetsSearch(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const query: string[] = [];
	if (filter) {
		query.push(`name contains '${filter.replace("'", "\\'")}'`);
	}
	query.push("mimeType = 'application/vnd.google-apps.spreadsheet'");

	const qs = {
		q: query.join(' and '),
		pageToken: (paginationToken as string) || undefined,
		fields: 'nextPageToken, files(id, name, webViewLink)',
		orderBy: 'modifiedByMeTime desc,name_natural',
		includeItemsFromAllDrives: true,
		supportsAllDrives: true,
	};

	const res = await apiRequest.call(
		this,
		'GET',
		'',
		{},
		qs,
		'https://www.googleapis.com/drive/v3/files',
	);
	return {
		results: res.files.map((sheet: IDataObject) => ({
			name: sheet.name as string,
			value: sheet.id as string,
			url: sheet.webViewLink as string,
		})),
		paginationToken: res.nextPageToken,
	};
}

export async function sheetsSearch(
	this: ILoadOptionsFunctions,
	_filter?: string,
): Promise<INodeListSearchResult> {
	const documentId = this.getNodeParameter('documentId', 0) as IDataObject | null;

	if (!documentId) return { results: [] };

	const { mode, value } = documentId;

	const spreadsheetId = getSpreadsheetId(this.getNode(), mode as ResourceLocator, value as string);

	const query = {
		fields: 'sheets.properties',
	};

	const responseData = await apiRequest.call(
		this,
		'GET',
		`/v4/spreadsheets/${spreadsheetId}`,
		{},
		query,
	);

	if (responseData === undefined) {
		throw new NodeOperationError(this.getNode(), 'No data got returned');
	}

	const returnData: INodeListSearchItems[] = [];
	for (const sheet of responseData.sheets!) {
		if (sheet.properties!.sheetType !== 'GRID') {
			continue;
		}

		returnData.push({
			name: sheet.properties!.title as string,
			value: (sheet.properties!.sheetId as number) || 'gid=0',
			url: `https://docs.google.com/spreadsheets/d/${spreadsheetId}/edit#gid=${sheet.properties!.sheetId}`,
		});
	}

	return { results: returnData };
}
