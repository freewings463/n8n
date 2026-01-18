"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Bannerbear/TemplateDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Bannerbear 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:templateOperations、templateFields。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Bannerbear/TemplateDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Bannerbear/TemplateDescription.py

import type { INodeProperties } from 'n8n-workflow';

export const templateOperations: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['template'],
			},
		},
		options: [
			{
				name: 'Get',
				value: 'get',
				description: 'Get a template',
				action: 'Get a template',
			},
			{
				name: 'Get Many',
				value: 'getAll',
				description: 'Get many templates',
				action: 'Get many templates',
			},
		],
		default: 'get',
	},
];

export const templateFields: INodeProperties[] = [
	/* -------------------------------------------------------------------------- */
	/*                                 template:get                               */
	/* -------------------------------------------------------------------------- */
	{
		displayName: 'Template ID',
		name: 'templateId',
		type: 'string',
		required: true,
		default: '',
		displayOptions: {
			show: {
				resource: ['template'],
				operation: ['get'],
			},
		},
		description: 'Unique identifier for the template',
	},
];
