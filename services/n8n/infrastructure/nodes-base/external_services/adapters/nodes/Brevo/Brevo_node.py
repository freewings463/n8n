"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Brevo/Brevo.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Brevo 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./AttributeDescription、./ContactDescription、./EmailDescription、./SenderDescrition。导出:Brevo。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-filename-against-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Brevo/Brevo.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Brevo/Brevo_node.py

/* eslint-disable n8n-nodes-base/node-filename-against-convention */
import type { INodeType, INodeTypeDescription } from 'n8n-workflow';
import { NodeConnectionTypes } from 'n8n-workflow';

import { attributeFields, attributeOperations } from './AttributeDescription';
import { contactFields, contactOperations } from './ContactDescription';
import { emailFields, emailOperations } from './EmailDescription';
import { senderFields, senderOperations } from './SenderDescrition';

export class Brevo implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Brevo',
		// keep sendinblue name for backward compatibility
		name: 'sendInBlue',
		icon: 'file:brevo.svg',
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Consume Brevo API',
		defaults: {
			name: 'Brevo',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'sendInBlueApi',
				required: true,
			},
		],
		requestDefaults: {
			baseURL: 'https://api.brevo.com',
		},
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Contact',
						value: 'contact',
					},
					{
						name: 'Contact Attribute',
						value: 'attribute',
					},
					{
						name: 'Email',
						value: 'email',
					},
					{
						name: 'Sender',
						value: 'sender',
					},
				],
				default: 'email',
			},

			...attributeOperations,
			...attributeFields,
			...senderOperations,
			...senderFields,
			...contactOperations,
			...contactFields,
			...emailOperations,
			...emailFields,
		],
	};
}
