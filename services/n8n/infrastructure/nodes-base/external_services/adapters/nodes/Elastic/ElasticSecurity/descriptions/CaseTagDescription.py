"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Elastic/ElasticSecurity/descriptions/CaseTagDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Elastic/ElasticSecurity 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:caseTagOperations、caseTagFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Elastic/ElasticSecurity/descriptions/CaseTagDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Elastic/ElasticSecurity/descriptions/CaseTagDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const caseTagOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['caseTag'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				description: 'Add a tag to a case',
				action: 'Add a tag to a case',
			},
			{
				name: 'Remove',
				value: 'remove',
				description: 'Remove a tag from a case',
				action: 'Remove a tag from a case',
			},
		],
		default: 'add',
	},
];

export const caseTagFields: INodeProperties[] = [
	// ----------------------------------------
	//             caseTag: add
	// ----------------------------------------
	{
		displayName: 'Case ID',
		name: 'caseId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['caseTag'],
				operation: ['add'],
			},
		},
	},
	{
		displayName: 'Tag Name or ID',
		name: 'tag',
		type: 'options',
		description:
			'Tag to attach to the case. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
		required: true,
		default: '',
		typeOptions: {
			loadOptionsMethod: 'getTags',
		},
		displayOptions: {
			show: {
				resource: ['caseTag'],
				operation: ['add'],
			},
		},
	},

	// ----------------------------------------
	//            caseTag: remove
	// ----------------------------------------
	{
		displayName: 'Case ID',
		name: 'caseId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['caseTag'],
				operation: ['remove'],
			},
		},
	},
	{
		displayName: 'Tag Name or ID',
		name: 'tag',
		type: 'options',
		description:
			'Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>',
		required: true,
		default: '',
		typeOptions: {
			loadOptionsMethod: 'getTags',
		},
		displayOptions: {
			show: {
				resource: ['caseTag'],
				operation: ['remove'],
			},
		},
	},
];
