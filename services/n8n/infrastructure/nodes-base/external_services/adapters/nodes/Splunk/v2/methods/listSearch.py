"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Splunk/v2/methods/listSearch.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Splunk/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../transport。导出:无。关键函数/方法:searchReports、searchJobs、searchUsers。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Splunk/v2/methods/listSearch.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Splunk/v2/methods/listSearch.py

import type { IDataObject, ILoadOptionsFunctions, INodeListSearchResult } from 'n8n-workflow';

import { splunkApiJsonRequest } from '../transport';

export async function searchReports(
	this: ILoadOptionsFunctions,
	filter?: string,
): Promise<INodeListSearchResult> {
	const qs: IDataObject = {};

	if (filter) {
		qs.search = filter;
	}

	const endpoint = '/services/saved/searches';
	const response = await splunkApiJsonRequest.call(this, 'GET', endpoint, undefined, qs);

	return {
		results: (response as IDataObject[]).map((entry: IDataObject) => {
			return {
				name: entry.name as string,
				value: entry.id as string,
				url: entry.entryUrl as string,
			};
		}),
	};
}

export async function searchJobs(
	this: ILoadOptionsFunctions,
	filter?: string,
): Promise<INodeListSearchResult> {
	const qs: IDataObject = {};

	if (filter) {
		qs.search = filter;
	}

	const endpoint = '/services/search/jobs';
	const response = await splunkApiJsonRequest.call(this, 'GET', endpoint, undefined, qs);

	return {
		results: (response as IDataObject[]).map((entry: IDataObject) => {
			return {
				name: (entry.name as string).replace(/^\|\s*/, ''),
				value: entry.id as string,
				url: entry.entryUrl as string,
			};
		}),
	};
}

export async function searchUsers(
	this: ILoadOptionsFunctions,
	filter?: string,
): Promise<INodeListSearchResult> {
	const qs: IDataObject = {};

	if (filter) {
		qs.search = filter;
	}

	const endpoint = '/services/authentication/users';
	const response = await splunkApiJsonRequest.call(this, 'GET', endpoint, undefined, qs);

	return {
		results: (response as IDataObject[]).map((entry: IDataObject) => {
			return {
				name: entry.name as string,
				value: entry.id as string,
				url: entry.entryUrl as string,
			};
		}),
	};
}
