"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Onfleet/descriptions/OnfleetWebhookDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Onfleet/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../WebhookMapping。导出:eventDisplay、eventNameField。关键函数/方法:sort。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Onfleet/descriptions/OnfleetWebhookDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Onfleet/descriptions/OnfleetWebhookDescription.py

import type { INodeProperties } from 'n8n-workflow';

import { webhookMapping } from '../WebhookMapping';

const sort = (a: { name: string }, b: { name: string }) => {
	if (a.name < b.name) {
		return -1;
	}
	if (a.name > b.name) {
		return 1;
	}
	return 0;
};

export const eventDisplay: INodeProperties = {
	displayName: 'Trigger On',
	name: 'triggerOn',
	type: 'options',
	options: Object.keys(webhookMapping)
		.map((webhook) => {
			const { name, value } = webhookMapping[webhook];
			return { name, value };
		})
		.sort(sort),
	required: true,
	default: [],
};

export const eventNameField = {
	displayName: 'Additional Fields',
	name: 'additionalFields',
	type: 'collection',
	placeholder: 'Add Field',
	default: {},
	options: [
		{
			displayName: 'Name',
			name: 'name',
			type: 'string',
			default: '',
			description: 'A name for the webhook for identification',
		},
	],
} as INodeProperties;
