"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/resources/issue/getAll.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/declarative 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../shared/utils。导出:issueGetManyDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/resources/issue/getAll.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/declarative/github-issues/template/nodes/GithubIssues/resources/issue/getAll.py

import type { INodeProperties } from 'n8n-workflow';
import { parseLinkHeader } from '../../shared/utils';

const showOnlyForIssueGetMany = {
	operation: ['getAll'],
	resource: ['issue'],
};

export const issueGetManyDescription: INodeProperties[] = [
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				...showOnlyForIssueGetMany,
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 100,
		},
		default: 50,
		routing: {
			send: {
				type: 'query',
				property: 'per_page',
			},
			output: {
				maxResults: '={{$value}}',
			},
		},
		description: 'Max number of results to return',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: showOnlyForIssueGetMany,
		},
		default: false,
		description: 'Whether to return all results or only up to a given limit',
		routing: {
			send: {
				paginate: '={{ $value }}',
				type: 'query',
				property: 'per_page',
				value: '100',
			},
			operations: {
				pagination: {
					type: 'generic',
					properties: {
						continue: `={{ !!(${parseLinkHeader.toString()})($response.headers?.link).next }}`,
						request: {
							url: `={{ (${parseLinkHeader.toString()})($response.headers?.link)?.next ?? $request.url }}`,
						},
					},
				},
			},
		},
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		typeOptions: {
			multipleValueButtonText: 'Add Filter',
		},
		displayOptions: {
			show: showOnlyForIssueGetMany,
		},
		default: {},
		options: [
			{
				displayName: 'Updated Since',
				name: 'since',
				type: 'dateTime',
				default: '',
				description: 'Return only issues updated at or after this time',
				routing: {
					request: {
						qs: {
							since: '={{$value}}',
						},
					},
				},
			},
			{
				displayName: 'State',
				name: 'state',
				type: 'options',
				options: [
					{
						name: 'All',
						value: 'all',
						description: 'Returns issues with any state',
					},
					{
						name: 'Closed',
						value: 'closed',
						description: 'Return issues with "closed" state',
					},
					{
						name: 'Open',
						value: 'open',
						description: 'Return issues with "open" state',
					},
				],
				default: 'open',
				description: 'The issue state to filter on',
				routing: {
					request: {
						qs: {
							state: '={{$value}}',
						},
					},
				},
			},
		],
	},
];
