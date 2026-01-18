"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/HumanticAI/ProfileDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/HumanticAI 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:profileOperations、profileFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/HumanticAI/ProfileDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/HumanticAI/ProfileDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const profileOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['profile'],
			},
		},
		options: [
			{
				name: 'Create',
				value: 'create',
				description: 'Create a profile',
				action: 'Create a profile',
			},
			{
				name: 'Get',
				value: 'get',
				description: 'Retrieve a profile',
				action: 'Get a profile',
			},
			{
				name: 'Update',
				value: 'update',
				description: 'Update a profile',
				action: 'Update a profile',
			},
		],
		default: 'create',
	},
];

export const profileFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 profile:create                             */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'User ID',
		name: 'userId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['profile'],
			},
		},
		description:
			'The LinkedIn profile URL or email ID for creating a Humantic profile. If you are sending the resume, this should be a unique string.',
	},
	{
		displayName: 'Send Resume',
		name: 'sendResume',
		type: 'boolean',
		default: false,
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['profile'],
			},
		},
		description: 'Whether to send a resume for a resume based analysis',
	},
	{
		displayName: 'Input Binary Field',
		name: 'binaryPropertyName',
		type: 'string',
		default: 'data',
		displayOptions: {
			show: {
				operation: ['create'],
				resource: ['profile'],
				sendResume: [true],
			},
		},
		hint: 'The name of the input binary field containing the resume in PDF or DOCX format',
	},

	/* -------------------------------------------------------------------------- */
	/*                                 profile:get                                */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'User ID',
		name: 'userId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['profile'],
			},
		},
		description:
			'This value is the same as the User ID that was provided when the analysis was created. This could be a LinkedIn URL, email ID, or a unique string in case of resume based analysis.',
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		placeholder: 'Add option',
		default: {},
		displayOptions: {
			show: {
				operation: ['get'],
				resource: ['profile'],
			},
		},
		options: [
			{
				displayName: 'Persona',
				name: 'persona',
				type: 'multiOptions',
				options: [
					{
						name: 'Sales',
						value: 'sales',
					},
					{
						name: 'Hiring',
						value: 'hiring',
					},
				],
				default: [],
				description:
					'Fetch the Humantic profile of the user for a particular persona type. Multiple persona values can be supported using comma as a delimiter.',
			},
		],
	},

	/* -------------------------------------------------------------------------- */
	/*                                 profile:update                             */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'User ID',
		name: 'userId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['profile'],
			},
		},
		description:
			'This value is the same as the User ID that was provided when the analysis was created. Currently only supported for profiles created using LinkedIn URL.',
	},
	{
		displayName: 'Send Resume',
		name: 'sendResume',
		type: 'boolean',
		default: false,
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['profile'],
			},
		},
		description: 'Whether to send a resume for a resume of the user',
	},
	{
		displayName: 'Text',
		name: 'text',
		type: 'string',
		default: '',
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['profile'],
				sendResume: [false],
			},
		},
		description: 'Additional text written by the user',
	},
	{
		displayName: 'Input Binary Field',
		name: 'binaryPropertyName',
		type: 'string',
		default: 'data',
		displayOptions: {
			show: {
				operation: ['update'],
				resource: ['profile'],
				sendResume: [true],
			},
		},
		hint: 'The name of the input binary field containing the resume in PDF or DOCX format',
	},
];
