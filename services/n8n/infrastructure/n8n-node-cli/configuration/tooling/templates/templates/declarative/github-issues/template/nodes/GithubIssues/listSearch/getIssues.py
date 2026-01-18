"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/listSearch/getIssues.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/declarative 的节点。导入/依赖:外部:无；内部:无；本地:../shared/transport。导出:无。关键函数/方法:getIssues。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/listSearch/getIssues.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/declarative/github-issues/template/nodes/GithubIssues/listSearch/getIssues.py

import type {
	ILoadOptionsFunctions,
	INodeListSearchResult,
	INodeListSearchItems,
} from 'n8n-workflow';
import { githubApiRequest } from '../shared/transport';

type IssueSearchItem = {
	number: number;
	title: string;
	html_url: string;
};

type IssueSearchResponse = {
	items: IssueSearchItem[];
	total_count: number;
};

export async function getIssues(
	this: ILoadOptionsFunctions,
	filter?: string,
	paginationToken?: string,
): Promise<INodeListSearchResult> {
	const page = paginationToken ? +paginationToken : 1;
	const per_page = 100;

	let responseData: IssueSearchResponse = {
		items: [],
		total_count: 0,
	};
	const owner = this.getNodeParameter('owner', '', { extractValue: true });
	const repository = this.getNodeParameter('repository', '', { extractValue: true });
	const filters = [filter, `repo:${owner}/${repository}`];

	responseData = await githubApiRequest.call(this, 'GET', '/search/issues', {
		q: filters.filter(Boolean).join(' '),
		page,
		per_page,
	});

	const results: INodeListSearchItems[] = responseData.items.map((item: IssueSearchItem) => ({
		name: item.title,
		value: item.number,
		url: item.html_url,
	}));

	const nextPaginationToken = page * per_page < responseData.total_count ? page + 1 : undefined;
	return { results, paginationToken: nextPaginationToken };
}
