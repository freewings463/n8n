"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/resources/issueComment/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/declarative 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:../shared/descriptions、./getAll。导出:issueCommentDescription。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/resources/issueComment/index.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/declarative/github-issues/template/nodes/GithubIssues/resources/issueComment/__init__.py

import type { INodeProperties } from 'n8n-workflow';
import { repoNameSelect, repoOwnerSelect } from '../../shared/descriptions';
import { issueCommentGetManyDescription } from './getAll';

const showOnlyForIssueComments = {
	resource: ['issueComment'],
};

export const issueCommentDescription: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: showOnlyForIssueComments,
		},
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get issue comments',
				description: 'Get issue comments',
				routing: {
					request: {
						method: 'GET',
						url: '=/repos/{{$parameter.owner}}/{{$parameter.repository}}/issues/comments',
					},
				},
			},
		],
		default: 'getAll',
	},
	{
		...repoOwnerSelect,
		displayOptions: {
			show: showOnlyForIssueComments,
		},
	},
	{
		...repoNameSelect,
		displayOptions: {
			show: showOnlyForIssueComments,
		},
	},
	...issueCommentGetManyDescription,
];
