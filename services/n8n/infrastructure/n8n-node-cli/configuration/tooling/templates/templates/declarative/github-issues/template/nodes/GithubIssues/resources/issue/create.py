"""
MIGRATION-META:
  source_path: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/resources/issue/create.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/node-cli/src/template/templates/declarative 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:issueCreateDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - node-cli templates -> infrastructure/configuration/tooling/templates
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/node-cli/src/template/templates/declarative/github-issues/template/nodes/GithubIssues/resources/issue/create.ts -> services/n8n/infrastructure/n8n-node-cli/configuration/tooling/templates/templates/declarative/github-issues/template/nodes/GithubIssues/resources/issue/create.py

import type { INodeProperties } from 'n8n-workflow';

const showOnlyForIssueCreate = {
	operation: ['create'],
	resource: ['issue'],
};

export const issueCreateDescription: INodeProperties[] = [
	{
		displayName: 'Title',
		name: 'title',
		type: 'string',
		default: '',
		required: true,
		displayOptions: {
			show: showOnlyForIssueCreate,
		},
		description: 'The title of the issue',
		routing: {
			send: {
				type: 'body',
				property: 'title',
			},
		},
	},
	{
		displayName: 'Body',
		name: 'body',
		type: 'string',
		typeOptions: {
			rows: 5,
		},
		default: '',
		displayOptions: {
			show: showOnlyForIssueCreate,
		},
		description: 'The body of the issue',
		routing: {
			send: {
				type: 'body',
				property: 'body',
			},
		},
	},
	{
		displayName: 'Labels',
		name: 'labels',
		type: 'collection',
		typeOptions: {
			multipleValues: true,
			multipleValueButtonText: 'Add Label',
		},
		displayOptions: {
			show: showOnlyForIssueCreate,
		},
		default: { label: '' },
		options: [
			{
				displayName: 'Label',
				name: 'label',
				type: 'string',
				default: '',
				description: 'Label to add to issue',
			},
		],
		routing: {
			send: {
				type: 'body',
				property: 'labels',
				value: '={{$value.map((data) => data.label)}}',
			},
		},
	},
];
