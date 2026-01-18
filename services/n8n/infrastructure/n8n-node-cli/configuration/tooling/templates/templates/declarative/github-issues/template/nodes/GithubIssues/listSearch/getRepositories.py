"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/listSearch/getRepositories.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/declarative 的节点。导入/依赖:外部:无；内部:无；本地:../shared/transport。导出:无。关键函数/方法:getRepositories。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/listSearch/getRepositories.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/declarative/github-issues/template/nodes/GithubIssues/listSearch/getRepositories.py

import type {
	ILoadOptionsFunctions,
	INodeListSearchItems,
	INodeListSearchResult,
} from 'n8n-workflow';
import { githubApiRequest } from '../shared/transport';

type RepositorySearchItem = {
	name: string;
	html_url: string;
};

type RepositorySearchResponse = {
	items: RepositorySearchItem[];
	total_count: number;
};

export async function getRepositories(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const owner = this.getCurrentNodeParameter('owner', { extractValue: true });
	const page = paginationToken ? +paginationToken : 1;
	const per_page = 100;
	const q = `${filter ?? ''} user:${owner} fork:true`;
	let responseData: RepositorySearchResponse = {
		items: [],
		total_count: 0,
	};

	try {
		responseData = await githubApiRequest.call(this, 'GET', '/search/repositories', {
			q,
			page,
			per_page,
		});
	} catch {
		// will fail if the owner does not have any repositories
	}

	const results: INodeListSearchItems[] = responseData.items.map((item: RepositorySearchItem) => ({
		name: item.name,
		value: item.name,
		url: item.html_url,
	}));

	const nextPaginationToken = page * per_page < responseData.total_count ? page + 1 : undefined;
	return { results, paginationToken: nextPaginationToken };
}
