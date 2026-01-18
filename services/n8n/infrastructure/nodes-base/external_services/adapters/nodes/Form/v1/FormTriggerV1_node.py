"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Form/v1/FormTriggerV1.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Form/v1 的节点。导入/依赖:外部:无；内部:无；本地:../utils/utils。导出:FormTriggerV1。关键函数/方法:webhook。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Form/v1/FormTriggerV1.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Form/v1/FormTriggerV1_node.py

import {
	FORM_TRIGGER_PATH_IDENTIFIER,
	NodeConnectionTypes,
	type INodeType,
	type INodeTypeBaseDescription,
	type INodeTypeDescription,
	type IWebhookFunctions,
} from 'n8n-workflow';

import {
	formDescription,
	formFields,
	formRespondMode,
	formTitle,
	formTriggerPanel,
	webhookPath,
} from '../common.descriptions';
import { formWebhook } from '../utils/utils';

const descriptionV1: INodeTypeDescription = {
	displayName: 'n8n Form Trigger',
	name: 'formTrigger',
	icon: 'file:form.svg',
	group: ['trigger'],
	version: 1,
	description: 'Generate webforms in n8n and pass their responses to the workflow',
	defaults: {
		name: 'n8n Form Trigger',
	},

	inputs: [],
	outputs: [NodeConnectionTypes.Main],
	webhooks: [
		{
			name: 'setup',
			httpMethod: 'GET',
			responseMode: 'onReceived',
			isFullPath: true,
			path: `={{$parameter["path"]}}/${FORM_TRIGGER_PATH_IDENTIFIER}`,
			ndvHideUrl: true,
		},
		{
			name: 'default',
			httpMethod: 'POST',
			responseMode: '={{$parameter["responseMode"]}}',
			responseData: '={{$parameter["responseMode"] === "lastNode" ? "noData" : undefined}}',
			isFullPath: true,
			path: `={{$parameter["path"]}}/${FORM_TRIGGER_PATH_IDENTIFIER}`,
			ndvHideMethod: true,
		},
	],
	eventTriggerDescription: 'Waiting for you to submit the form',
	activationMessage: 'You can now make calls to your production Form URL.',
	triggerPanel: formTriggerPanel,
	properties: [
		webhookPath,
		formTitle,
		formDescription,
		formFields,
		formRespondMode,
		{
			displayName: 'Options',
			name: 'options',
			type: 'collection',
			placeholder: 'Add option',
			default: {},
			displayOptions: {
				hide: {
					responseMode: ['responseNode'],
				},
			},
			options: [
				{
					displayName: 'Form Submitted Text',
					name: 'formSubmittedText',
					description: 'The text displayed to users after they filled the form',
					type: 'string',
					default: 'Your response has been recorded',
				},
			],
		},
	],
};

export class FormTriggerV1 implements INodeType {
	description: INodeTypeDescription;

	constructor(baseDescription: INodeTypeBaseDescription) {
		this.description = {
			...baseDescription,
			...descriptionV1,
		};
	}

	async webhook(this: IWebhookFunctions) {
		return await formWebhook(this);
	}
}
