"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/MistralAI/descriptions/document/Document.resource.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/MistralAI/descriptions 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./extractText.operation。导出:description。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/MistralAI/descriptions/document/Document.resource.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/MistralAI/descriptions/document/Document_resource.py

import type { INodeProperties } from 'n8n-workflow';

import * as extractText from './extractText.operation';

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		displayOptions: {
			show: {
				resource: ['document'],
			},
		},
		options: [
			{
				name: 'Extract Text',
				value: 'extractText',
				description: 'Extract text from document using OCR',
				action: 'Extract text',
			},
		],
		default: 'extractText',
	},

	...extractText.description,
];
