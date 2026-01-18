"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/N8n/N8n.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/N8n 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./AuditDescription、./CredentialDescription、./ExecutionDescription、./WorkflowDescription 等1项。导出:N8n。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/N8n/N8n.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/N8n/N8n_node.py

import { NodeConnectionTypes, type INodeType, type INodeTypeDescription } from 'n8n-workflow';

import { auditFields, auditOperations } from './AuditDescription';
import { credentialFields, credentialOperations } from './CredentialDescription';
import { executionFields, executionOperations } from './ExecutionDescription';
import { workflowFields, workflowOperations } from './WorkflowDescription';
import { searchWorkflows } from './WorkflowLocator';

/**
 * The n8n node provides access to the n8n API.
 *
 * See: https://docs.n8n.io/api/api-reference/
 */
export class N8n implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'n8n',
		name: 'n8n',
		icon: 'file:n8n.svg',
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Handle events and perform actions on your n8n instance',
		defaults: {
			name: 'n8n',
		},
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'n8nApi',
				required: true,
			},
		],
		requestDefaults: {
			returnFullResponse: true,
			baseURL: '={{ $credentials.baseUrl.replace(new RegExp("/$"), "") }}',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
			},
		},
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Audit',
						value: 'audit',
					},
					{
						name: 'Credential',
						value: 'credential',
					},
					{
						name: 'Execution',
						value: 'execution',
					},
					{
						name: 'Workflow',
						value: 'workflow',
					},
				],
				default: 'workflow',
			},

			...auditOperations,
			...auditFields,

			...credentialOperations,
			...credentialFields,

			...executionOperations,
			...executionFields,

			...workflowOperations,
			...workflowFields,
		],
	};

	methods = {
		listSearch: {
			// Provide workflows search capability for the workflow resourceLocator
			searchWorkflows,
		},
	};
}
