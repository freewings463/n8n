"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtop/actions/extraction/query.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtop/actions 的节点。导入/依赖:外部:无；内部:无；本地:../common/fields、../common/output.utils、../common/session.utils。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtop/actions/extraction/query.operation.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtop/actions/extraction/query_operation.py

import {
	type IExecuteFunctions,
	type INodeExecutionData,
	type INodeProperties,
} from 'n8n-workflow';

import { outputSchemaField, parseJsonOutputField } from '../common/fields';
import { parseJsonIfPresent } from '../common/output.utils';
import { executeRequestWithSessionManagement } from '../common/session.utils';

export const description: INodeProperties[] = [
	{
		displayName: 'Prompt',
		name: 'prompt',
		type: 'string',
		typeOptions: {
			rows: 4,
		},
		required: true,
		default: '',
		placeholder: 'e.g. Is there a login form in this page?',
		displayOptions: {
			show: {
				resource: ['extraction'],
				operation: ['query'],
			},
		},
		description: 'The prompt to query the page content',
	},
	{
		displayName: 'Additional Fields',
		name: 'additionalFields',
		type: 'collection',
		placeholder: 'Add Field',
		default: {},
		displayOptions: {
			show: {
				resource: ['extraction'],
				operation: ['query'],
			},
		},
		options: [
			{
				...outputSchemaField,
			},
			{
				...parseJsonOutputField,
			},
			{
				displayName: 'Include Visual Analysis',
				name: 'includeVisualAnalysis',
				type: 'boolean',
				default: false,
				description: 'Whether to analyze the web page visually when fulfilling the request',
			},
		],
	},
];

export async function execute(
	this: IExecuteFunctions,
	index: number,
): Promise<INodeExecutionData[]> {
	const prompt = this.getNodeParameter('prompt', index, '') as string;
	const additionalFields = this.getNodeParameter('additionalFields', index, {});
	const outputSchema = additionalFields.outputSchema;
	const includeVisualAnalysis = additionalFields.includeVisualAnalysis;

	const result = await executeRequestWithSessionManagement.call(this, index, {
		method: 'POST',
		path: '/sessions/{sessionId}/windows/{windowId}/page-query',
		body: {
			prompt,
			configuration: {
				experimental: {
					includeVisualAnalysis: includeVisualAnalysis ? 'enabled' : 'disabled',
				},
				...(outputSchema ? { outputSchema } : {}),
			},
		},
	});

	const nodeOutput = parseJsonIfPresent.call(this, index, result);
	return this.helpers.returnJsonArray(nodeOutput);
}
