"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/resources/issue/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/declarative 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:../shared/descriptions、./getAll、./get、./create。导出:issueDescription。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/resources/issue/index.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/declarative/github-issues/template/nodes/GithubIssues/resources/issue/__init__.py

import type { INodeProperties } from 'n8n-workflow';
import { repoNameSelect, repoOwnerSelect } from '../../shared/descriptions';
import { issueGetManyDescription } from './getAll';
import { issueGetDescription } from './get';
import { issueCreateDescription } from './create';

const showOnlyForIssues = {
	resource: ['issue'],
};

export const issueDescription: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: showOnlyForIssues,
		},
		options: [
			{
				name: 'Get Many',
				value: 'getAll',
				action: 'Get issues in a repository',
				description: 'Get many issues in a repository',
				routing: {
					request: {
						method: 'GET',
						url: '=/repos/{{$parameter.owner}}/{{$parameter.repository}}/issues',
					},
				},
			},
			{
				name: 'Get',
				value: 'get',
				action: 'Get an issue',
				description: 'Get the data of a single issue',
				routing: {
					request: {
						method: 'GET',
						url: '=/repos/{{$parameter.owner}}/{{$parameter.repository}}/issues/{{$parameter.issue}}',
					},
				},
			},
			{
				name: 'Create',
				value: 'create',
				action: 'Create a new issue',
				description: 'Create a new issue',
				routing: {
					request: {
						method: 'POST',
						url: '=/repos/{{$parameter.owner}}/{{$parameter.repository}}/issues',
					},
				},
			},
		],
		default: 'getAll',
	},
	{
		...repoOwnerSelect,
		displayOptions: {
			show: showOnlyForIssues,
		},
	},
	{
		...repoNameSelect,
		displayOptions: {
			show: showOnlyForIssues,
		},
	},
	...issueGetManyDescription,
	...issueGetDescription,
	...issueCreateDescription,
];
