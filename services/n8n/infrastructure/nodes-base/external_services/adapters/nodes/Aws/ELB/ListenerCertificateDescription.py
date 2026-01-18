"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Aws/ELB/ListenerCertificateDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Aws/ELB 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:listenerCertificateOperations、listenerCertificateFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Aws/ELB/ListenerCertificateDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Aws/ELB/ListenerCertificateDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const listenerCertificateOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['listenerCertificate'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				description:
					'Add the specified SSL server certificate to the certificate list for the specified HTTPS or TLS listener',
				action: 'Add a listener certificate',
			},
			{
				name: 'Get Many',
				value: 'getMany',
				description: 'Get many listener certificates',
				action: 'Get many listener certificates',
			},
			{
				name: 'Remove',
				value: 'remove',
				description:
					'Remove the specified certificate from the certificate list for the specified HTTPS or TLS listener',
				action: 'Remove a listener certificate',
			},
		],
		default: 'add',
	},
];

export const listenerCertificateFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                listenerCertificate:add                     */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Load Balancer ARN Name or ID',
		name: 'loadBalancerId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getLoadBalancers',
		},
		required: true,
		displayOptions: {
			show: {
				resource: ['listenerCertificate'],
				operation: ['add'],
			},
		},
		default: '',
		description:
			'Unique identifier for a particular loadBalancer. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Listener ARN Name or ID',
		name: 'listenerId',
		type: 'options',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getLoadBalancerListeners',
			loadOptionsDependsOn: ['loadBalancerId'],
		},
		displayOptions: {
			show: {
				resource: ['listenerCertificate'],
				operation: ['add'],
			},
		},
		default: '',
		description:
			'Unique identifier for a particular loadBalancer. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Certificate ARN',
		name: 'certificateId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['listenerCertificate'],
				operation: ['add'],
			},
		},
		default: '',
		description: 'Unique identifier for a particular loadBalancer',
	},

	/* -------------------------------------------------------------------------- */
	/*                              listenerCertificate:getMany                    */
	/* -------------------------------------------------------------------------- */

	{
		displayName: 'Load Balancer ARN Name or ID',
		name: 'loadBalancerId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getLoadBalancers',
		},
		required: true,
		displayOptions: {
			show: {
				resource: ['listenerCertificate'],
				operation: ['getMany'],
			},
		},
		default: '',
		description:
			'Unique identifier for a particular loadBalancer. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Listener ARN Name or ID',
		name: 'listenerId',
		type: 'options',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getLoadBalancerListeners',
			loadOptionsDependsOn: ['loadBalancerId'],
		},
		displayOptions: {
			show: {
				resource: ['listenerCertificate'],
				operation: ['getMany'],
			},
		},
		default: '',
		description:
			'Unique identifier for a particular loadBalancer. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Return All',
		name: 'returnAll',
		type: 'boolean',
		displayOptions: {
			show: {
				resource: ['listenerCertificate'],
				operation: ['getMany'],
			},
		},
		default: false,
		description: 'Whether to return all results or only up to a given limit',
	},
	{
		displayName: 'Limit',
		name: 'limit',
		type: 'number',
		description: 'Max number of results to return',
		default: 100,
		typeOptions: {
			maxValue: 400,
			minValue: 1,
		},
		displayOptions: {
			show: {
				resource: ['listenerCertificate'],
				operation: ['getMany'],
				returnAll: [false],
			},
		},
	},

	/* -------------------------------------------------------------------------- */
	/*                                listenerCertificate:remove                  */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Load Balancer ARN Name or ID',
		name: 'loadBalancerId',
		type: 'options',
		typeOptions: {
			loadOptionsMethod: 'getLoadBalancers',
		},
		required: true,
		displayOptions: {
			show: {
				resource: ['listenerCertificate'],
				operation: ['remove'],
			},
		},
		default: '',
		description:
			'Unique identifier for a particular loadBalancer. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Listener ARN Name or ID',
		name: 'listenerId',
		type: 'options',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getLoadBalancerListeners',
			loadOptionsDependsOn: ['loadBalancerId'],
		},
		displayOptions: {
			show: {
				resource: ['listenerCertificate'],
				operation: ['remove'],
			},
		},
		default: '',
		description:
			'Unique identifier for a particular loadBalancer. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Certificate ARN',
		name: 'certificateId',
		type: 'string',
		required: true,
		displayOptions: {
			show: {
				resource: ['listenerCertificate'],
				operation: ['remove'],
			},
		},
		default: '',
		description: 'Unique identifier for a particular loadBalancer',
	},
];
