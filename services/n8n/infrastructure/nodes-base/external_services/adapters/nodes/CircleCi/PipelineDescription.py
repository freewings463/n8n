"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/CircleCi/PipelineDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/CircleCi 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:pipelineOperations、pipelineFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/CircleCi/PipelineDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/CircleCi/PipelineDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const pipelineOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['pipeline'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get a pipeline',
				action: 'Get a pipeline',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many pipelines',
				action: 'Get many pipelines',
			},
			{
				name: 'Trigger',
				value: 'trigger',
				description: 'Trigger a pipeline',
				action: 'Trigger a pipeline',
			},
		],
		default: 'get',
	},
];

export const pipelineFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                               pipeline:shared                              */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Provider',
		name: 'vcs',
		type: 'options',
		options: [
			{
				name: 'Bitbucket',
				value: 'bitbucket',
			},
			{
				name: 'GitHub',
				value: 'github',
			},
		],
		displayOptions: {
			show: {
				operation: ['get', 'getAll', 'trigger'],
				resource: ['pipeline'],
			},
		},
		default: '',
		description: 'Source control system',
	},
	{
		displayName: 'Project Slug',
		name: 'projectSlug',
		type: 'string',
		displayOptions: {
			show: {
				operation: ['get', 'getAll', 'trigger'],
				resource: ['pipeline'],
			},
		},
		default: '',
		placeholder: 'n8n-io/n8n',
		description: 'Project slug in the form org-name/repo-name',
	},

	/* -------------------------------------------------------------------------- */
	/*                                 pipeline:get                               */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Pipeline Number',
		name: 'pipelineNumber',
		type: 'number',
		typeOptions: {
			minValue: 1,
		},
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['pipeline'],
			},
		},
		default: 1,
		description: 'The number of the pipeline',
	},

	/* -------------------------------------------------------------------------- */
	/*                                 pipeline:getAll                            */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['pipeline'],
			},
		},
		default: false,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		displayOptions: {
			show: {
				operation: ['getAll'],
				resource: ['pipeline'],
				returnAll: [false],
			},
		},
		typeOptions: {
			minValue: 1,
			maxValue: 500,
		},
		default: 100,
		description: 'Max number of results to return',
	},
	{
		displayName: 'Filters',
		name: 'filters',
		type: 'collection',
		placeholder: 'Add Filter',
		default: {},
		displayOptions: {
			show: {
				resource: ['pipeline'],
				operation: ['getAll'],
			},
		},
		options: [
			{
				displayName: 'Branch',
				name: 'branch',
				type: 'string',
				default: '',
				description: 'The name of a vcs branch',
			},
		],
	},

	/* -------------------------------------------------------------------------- */
	/*                                 pipeline:trigger                           */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['pipeline'],
				operation: ['trigger'],
			},
		},
		options: [
			{
				displayName: 'Branch',
				name: 'branch',
				type: 'string',
				default: '',
				description:
					'The branch where the pipeline ran. The HEAD commit on this branch was used for the pipeline. Note that branch and tag are mutually exclusive.',
			},
			{
				displayName: 'Tag',
				name: 'tag',
				type: 'string',
				default: '',
				description:
					'The tag used by the pipeline. The commit that this tag points to was used for the pipeline. Note that branch and tag are mutually exclusive',
			},
		],
	},
];
