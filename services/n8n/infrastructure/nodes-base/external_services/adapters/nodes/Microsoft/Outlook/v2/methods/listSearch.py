"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/Outlook/v2/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/Outlook 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../helpers/utils、../transport。导出:无。关键函数/方法:search、searchContacts、searchCalendars、searchDrafts、searchMessages、searchEvents、searchFolders、searchAttachments。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/Outlook/v2/methods/listSearch.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/Outlook/v2/methods/listSearch.py

import type { IDataObject, ILoadOptionsFunctions, INodeListSearchResult } from 'n8n-workflow';

import { encodeOutlookId } from '../helpers/utils';
import { getSubfolders, microsoftApiRequest } from '../transport';

async function search(
	this: ILoadOptionsFunctions,
	resource: string,
	nameProperty: string,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
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
		const qs: IDataObject = {
			$select: `id,${nameProperty}`,
			$top: 100,
		};

		if (filter) {
			const filterValue = encodeURI(filter);
			qs.$filter = `contains(${nameProperty}, '${filterValue}')`;
		}

		response = await microsoftApiRequest.call(this, 'GET', resource, undefined, qs);
	}

	return {
		results: (response.value as IDataObject[]).map((entry: IDataObject) => {
			return {
				name: entry[nameProperty] as string,
				value: entry.id as string,
			};
		}),
		paginationToken: response['@odata.nextLink'],
	};
}

export async function searchContacts(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	return await search.call(this, '/contacts', 'displayName', filter, paginationToken);
}

export async function searchCalendars(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	return await search.call(this, '/calendars', 'name', filter, paginationToken);
}

export async function searchDrafts(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
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
		const qs: IDataObject = {
			$select: 'id,subject,bodyPreview,webLink',
			$top: 100,
			$filter: 'isDraft eq true',
		};

		if (filter) {
			const filterValue = encodeURI(filter);
			qs.$filter += ` AND contains(${'subject'}, '${filterValue}')`;
		}

		response = await microsoftApiRequest.call(this, 'GET', '/messages', undefined, qs);
	}

	return {
		results: (response.value as IDataObject[]).map((entry: IDataObject) => {
			return {
				name: (entry.subject || entry.bodyPreview) as string,
				value: entry.id as string,
				url: entry.webLink as string,
			};
		}),
		paginationToken: response['@odata.nextLink'],
	};
}

export async function searchMessages(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
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
		const qs: IDataObject = {
			$select: 'id,subject,bodyPreview,webLink',
			$top: 100,
		};

		if (filter) {
			const filterValue = encodeURI(filter);
			qs.$filter = `contains(${'subject'}, '${filterValue}')`;
		}

		response = await microsoftApiRequest.call(this, 'GET', '/messages', undefined, qs);
	}

	return {
		results: (response.value as IDataObject[]).map((entry: IDataObject) => {
			return {
				name: (entry.subject || entry.bodyPreview) as string,
				value: entry.id as string,
				url: entry.webLink as string,
			};
		}),
		paginationToken: response['@odata.nextLink'],
	};
}

export async function searchEvents(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	let response: IDataObject = {};

	const calendarId = this.getNodeParameter('calendarId', undefined, {
		extractValue: true,
	}) as string;

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
		const qs: IDataObject = {
			$select: 'id,subject,bodyPreview',
			$top: 100,
		};

		if (filter) {
			const filterValue = encodeURI(filter);
			qs.$filter = `contains(${'subject'}, '${filterValue}')`;
		}

		response = await microsoftApiRequest.call(
			this,
			'GET',
			`/calendars/${calendarId}/events`,
			undefined,
			qs,
		);
	}

	return {
		results: (response.value as IDataObject[]).map((entry: IDataObject) => {
			return {
				name: (entry.subject || entry.bodyPreview) as string,
				value: entry.id as string,
				url: `https://outlook.office365.com/calendar/item/${encodeOutlookId(entry.id as string)}`,
			};
		}),
		paginationToken: response['@odata.nextLink'],
	};
}

export async function searchFolders(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
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
		const qs: IDataObject = {
			$top: 100,
		};

		response = await microsoftApiRequest.call(this, 'GET', '/mailFolders', undefined, qs);
	}

	let folders = await getSubfolders.call(this, response.value as IDataObject[]);

	if (filter) {
		filter = filter.toLowerCase();
		folders = folders.filter((folder) =>
			((folder.displayName as string) || '').toLowerCase().includes(filter as string),
		);
	}

	return {
		results: folders.map((entry: IDataObject) => {
			return {
				name: entry.displayName as string,
				value: entry.id as string,
				url: `https://outlook.office365.com/mail/${encodeOutlookId(entry.id as string)}`,
			};
		}),
		paginationToken: response['@odata.nextLink'],
	};
}

export async function searchAttachments(
	this: ILoadOptionsFunctions,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	let response: IDataObject = {};

	const messageId = this.getNodeParameter('messageId', undefined, {
		extractValue: true,
	}) as string;

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
		const qs: IDataObject = {
			$select: 'id,name',
			$top: 100,
		};

		response = await microsoftApiRequest.call(
			this,
			'GET',
			`/messages/${messageId}/attachments`,
			undefined,
			qs,
		);
	}

	return {
		results: (response.value as IDataObject[]).map((entry: IDataObject) => {
			return {
				name: entry.name as string,
				value: entry.id as string,
			};
		}),
		paginationToken: response['@odata.nextLink'],
	};
}
