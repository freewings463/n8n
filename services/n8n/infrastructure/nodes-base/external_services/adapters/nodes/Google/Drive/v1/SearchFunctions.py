"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Drive/v1/SearchFunctions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Drive 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions。导出:无。关键函数/方法:fileSearch、folderSearch、driveSearch。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Drive/v1/SearchFunctions.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Drive/v1/SearchFunctions.py

import type { ILoadOptionsFunctions, INodeListSearchResult } from 'n8n-workflow';

import { googleApiRequest } from './GenericFunctions';

interface GoogleDriveFilesItem {
	id: string;
	name: string;
	mimeType: string;
	webViewLink: string;
}

interface GoogleDriveDriveItem {
	id: string;
	name: string;
}

export async function fileSearch(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const query: string[] = [];
	if (filter) {
		query.push(`name contains '${filter.replace("'", "\\'")}'`);
	}
	query.push("mimeType != 'application/vnd.google-apps.folder'");
	const res = await googleApiRequest.call(this, 'GET', '/drive/v3/files', undefined, {
		q: query.join(' and '),
		pageToken: paginationToken,
		fields: 'nextPageToken,files(id,name,mimeType,webViewLink)',
		orderBy: 'name_natural',
	});
	return {
		results: res.files.map((i: GoogleDriveFilesItem) => ({
			name: i.name,
			value: i.id,
			url: i.webViewLink,
		})),
		paginationToken: res.nextPageToken,
	};
}

export async function folderSearch(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const query: string[] = [];
	if (filter) {
		query.push(`name contains '${filter.replace("'", "\\'")}'`);
	}
	query.push("mimeType = 'application/vnd.google-apps.folder'");
	const res = await googleApiRequest.call(this, 'GET', '/drive/v3/files', undefined, {
		q: query.join(' and '),
		pageToken: paginationToken,
		fields: 'nextPageToken,files(id,name,mimeType,webViewLink)',
		orderBy: 'name_natural',
	});
	return {
		results: res.files.map((i: GoogleDriveFilesItem) => ({
			name: i.name,
			value: i.id,
			url: i.webViewLink,
		})),
		paginationToken: res.nextPageToken,
	};
}

export async function driveSearch(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const res = await googleApiRequest.call(this, 'GET', '/drive/v3/drives', undefined, {
		q: filter ? `name contains '${filter.replace("'", "\\'")}'` : undefined,
		pageToken: paginationToken,
	});
	return {
		results: res.drives.map((i: GoogleDriveDriveItem) => ({
			name: i.name,
			value: i.id,
		})),
		paginationToken: res.nextPageToken,
	};
}
