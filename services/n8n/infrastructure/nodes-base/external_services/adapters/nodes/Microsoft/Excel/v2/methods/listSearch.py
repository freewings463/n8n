"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Excel/v2/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Excel 的节点。导入/依赖:外部:无；内部:无；本地:../transport。导出:无。关键函数/方法:searchWorkbooks、getWorksheetsList、getWorksheetTables。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Excel/v2/methods/listSearch.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Excel/v2/methods/listSearch.py

import type {
	IDataObject,
	ILoadOptionsFunctions,
	INodeListSearchItems,
	INodeListSearchResult,
} from 'n8n-workflow';

import { microsoftApiRequest } from '../transport';

export async function searchWorkbooks(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const fileExtensions = ['.xlsx', '.xlsm', '.xlst'];
	const extensionFilter = fileExtensions.join(' OR ');

	const q = filter || extensionFilter;

	let response: IDataObject = {};

	if (paginationToken) {
		response = await microsoftApiRequest.call(
			this,
			'GET',
			'',
			undefined,
			undefined,
			paginationToken, // paginationToken contains the full URL
		);
	} else {
		response = await microsoftApiRequest.call(
			this,
			'GET',
			`/drive/root/search(q='${q}')`,
			undefined,
			{
				select: 'id,name,webUrl',
				$top: 100,
			},
		);
	}

	if (response.value && filter) {
		response.value = (response.value as IDataObject[]).filter((workbook: IDataObject) => {
			return fileExtensions.some((extension) => (workbook.name as string).includes(extension));
		});
	}

	return {
		results: (response.value as IDataObject[]).map((workbook: IDataObject) => {
			for (const extension of fileExtensions) {
				if ((workbook.name as string).includes(extension)) {
					workbook.name = (workbook.name as string).replace(extension, '');
					break;
				}
			}
			return {
				name: workbook.name as string,
				value: workbook.id as string,
				url: workbook.webUrl as string,
			};
		}),
		paginationToken: response['@odata.nextLink'],
	};
}

export async function getWorksheetsList(
	this: ILoadOptionsFunctions,
): Promise<INodeListSearchResult> {
	const workbookRLC = this.getNodeParameter('workbook') as IDataObject;
	const workbookId = workbookRLC.value as string;
	let workbookURL = (workbookRLC.cachedResultUrl as string) ?? '';

	if (workbookURL.includes('1drv.ms')) {
		workbookURL = `https://onedrive.live.com/edit.aspx?resid=${workbookId}`;
	}

	let response: IDataObject = {};

	response = await microsoftApiRequest.call(
		this,
		'GET',
		`/drive/items/${workbookId}/workbook/worksheets`,
		undefined,
		{
			select: 'id,name',
		},
	);

	return {
		results: (response.value as IDataObject[]).map((worksheet: IDataObject) => ({
			name: worksheet.name as string,
			value: worksheet.id as string,
			url: workbookURL
				? `${workbookURL}&activeCell=${encodeURIComponent(worksheet.name as string)}!A1`
				: undefined,
		})),
	};
}

export async function getWorksheetTables(
	this: ILoadOptionsFunctions,
): Promise<INodeListSearchResult> {
	const workbookRLC = this.getNodeParameter('workbook') as IDataObject;
	const workbookId = workbookRLC.value as string;
	let workbookURL = (workbookRLC.cachedResultUrl as string) ?? '';

	if (workbookURL.includes('1drv.ms')) {
		workbookURL = `https://onedrive.live.com/edit.aspx?resid=${workbookId}`;
	}

	const worksheetId = this.getNodeParameter('worksheet', undefined, {
		extractValue: true,
	}) as string;

	let response: IDataObject = {};

	response = await microsoftApiRequest.call(
		this,
		'GET',
		`/drive/items/${workbookId}/workbook/worksheets/${worksheetId}/tables`,
		undefined,
	);

	const results: INodeListSearchItems[] = [];

	for (const table of response.value as IDataObject[]) {
		const name = table.name as string;
		const value = table.id as string;

		const { address } = await microsoftApiRequest.call(
			this,
			'GET',
			`/drive/items/${workbookId}/workbook/worksheets/${worksheetId}/tables/${value}/range`,
			undefined,
			{
				select: 'address',
			},
		);

		const [sheetName, sheetRange] = address.split('!' as string);

		let url;
		if (workbookURL) {
			url = `${workbookURL}&activeCell=${encodeURIComponent(sheetName as string)}${
				sheetRange ? '!' + (sheetRange as string) : ''
			}`;
		}

		results.push({ name, value, url });
	}

	return { results };
}
