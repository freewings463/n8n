"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/GithubIssues.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/declarative 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./resources/issue、./resources/issueComment、./listSearch/getRepositories、./listSearch/getUsers 等1项。导出:GithubIssues。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/GithubIssues.node.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/declarative/github-issues/template/nodes/GithubIssues/GithubIssues_node.py

import { NodeConnectionTypes, type INodeType, type INodeTypeDescription } from 'n8n-workflow';
import { issueDescription } from './resources/issue';
import { issueCommentDescription } from './resources/issueComment';
import { getRepositories } from './listSearch/getRepositories';
import { getUsers } from './listSearch/getUsers';
import { getIssues } from './listSearch/getIssues';

export class GithubIssues implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'GitHub Issues',
		name: 'githubIssues',
		icon: { light: 'file:../../icons/github.svg', dark: 'file:../../icons/github.dark.svg' },
		group: ['input'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Consume issues from the GitHub API',
		defaults: {
			name: 'GitHub Issues',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'githubIssuesApi',
				required: true,
				displayOptions: {
					show: {
						authentication: ['accessToken'],
					},
				},
			},
			{
				name: 'githubIssuesOAuth2Api',
				required: true,
				displayOptions: {
					show: {
						authentication: ['oAuth2'],
					},
				},
			},
		],
		requestDefaults: {
			baseURL: 'https://api.github.com',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
			},
		},
		properties: [
			{
				displayName: 'Authentication',
				name: 'authentication',
				type: 'options',
				options: [
					{
						name: 'Access Token',
						value: 'accessToken',
					},
					{
						name: 'OAuth2',
						value: 'oAuth2',
					},
				],
				default: 'accessToken',
			},
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Issue',
						value: 'issue',
					},
					{
						name: 'Issue Comment',
						value: 'issueComment',
					},
				],
				default: 'issue',
			},
			...issueDescription,
			...issueCommentDescription,
		],
	};

	methods = {
		listSearch: {
			getRepositories,
			getUsers,
			getIssues,
		},
	};
}
