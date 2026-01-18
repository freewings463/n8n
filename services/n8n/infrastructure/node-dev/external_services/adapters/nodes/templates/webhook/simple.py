"""
MIGRATION-META:
  source_path: packages/node-dev/templates/webhook/simple.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/node-dev/templates/webhook 的Webhook模块。导入/依赖:外部:无；内部:无；本地:无。导出:ClassNameReplace。关键函数/方法:webhook。用于承载Webhook实现细节，并通过导出对外提供能力。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/node-dev/templates/webhook/simple.ts -> services/n8n/infrastructure/node-dev/external_services/adapters/nodes/templates/webhook/simple.py

import {
	IDataObject,
	IWebhookFunctions,
	INodeTypeDescription,
	INodeType,
	IWebhookResponseData,
} from 'n8n-workflow';

export class ClassNameReplace implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'DisplayNameReplace',
		name: 'N8nNameReplace',
		group: ['trigger'],
		version: 1,
		description: 'NodeDescriptionReplace',
		defaults: {
			name: 'DisplayNameReplace',
			color: '#885577',
		},
		inputs: [],
		outputs: ['main'],
		webhooks: [
			{
				name: 'default',
				httpMethod: 'POST',
				responseMode: 'onReceived',
				// Each webhook property can either be hardcoded
				// like the above ones or referenced from a parameter
				// like the "path" property bellow
				path: '={{$parameter["path"]}}',
			},
		],
		properties: [
			{
				displayName: 'Path',
				name: 'path',
				type: 'string',
				default: '',
				placeholder: '',
				required: true,
				description: 'The path to listen to',
			},
		],
	};

	async webhook(this: IWebhookFunctions): Promise<IWebhookResponseData> {
		// The data to return and so start the workflow with
		const returnData: IDataObject[] = [];
		returnData.push({
			headers: this.getHeaderData(),
			params: this.getParamsData(),
			query: this.getQueryData(),
			body: this.getBodyData(),
		});

		return {
			workflowData: [this.helpers.returnJsonArray(returnData)],
		};
	}
}
