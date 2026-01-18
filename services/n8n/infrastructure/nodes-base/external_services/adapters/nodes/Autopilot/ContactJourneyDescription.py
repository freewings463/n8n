"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Autopilot/ContactJourneyDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Autopilot 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:contactJourneyOperations、contactJourneyFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Autopilot/ContactJourneyDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Autopilot/ContactJourneyDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const contactJourneyOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['contactJourney'],
			},
		},
		options: [
			{
				name: 'Add',
				value: 'add',
				description: 'Add contact to list',
				action: 'Add a contact journey',
			},
		],
		default: 'add',
	},
];

export const contactJourneyFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 contactJourney:add                         */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Trigger Name or ID',
		name: 'triggerId',
		required: true,
		typeOptions: {
			loadOptionsMethod: 'getTriggers',
		},
		type: 'options',
		displayOptions: {
			show: {
				operation: ['add'],
				resource: ['contactJourney'],
			},
		},
		default: '',
		description:
			'List ID. Choose from the list, or specify an ID using an <a href="https://docs.n8n.io/code/expressions/">expression</a>.',
	},
	{
		displayName: 'Contact ID',
		name: 'contactId',
		required: true,
		type: 'string',
		displayOptions: {
			show: {
				operation: ['add'],
				resource: ['contactJourney'],
			},
		},
		default: '',
		description: 'Can be ID or email',
	},
];
