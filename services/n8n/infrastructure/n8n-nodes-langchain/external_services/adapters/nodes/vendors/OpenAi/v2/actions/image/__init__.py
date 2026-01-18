"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v2/actions/image/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./analyze.operation、./generate.operation、./edit.operation。导出:generate、analyze、edit、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v2/actions/image/index.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/v2/actions/image/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as analyze from './analyze.operation';
import * as generate from './generate.operation';
import * as edit from './edit.operation';

export { generate, analyze, edit };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Analyze Image',
				value: 'analyze',
				action: 'Analyze image',
				description: 'Take in images and answer questions about them',
			},
			{
				name: 'Generate an Image',
				value: 'generate',
				action: 'Generate an image',
				description: 'Creates an image from a text prompt',
			},
			{
				name: 'Edit Image',
				value: 'edit',
				action: 'Edit image',
				description: 'Edit an image',
			},
		],
		default: 'generate',
		displayOptions: {
			show: {
				resource: ['image'],
			},
		},
	},
	...generate.description,
	...analyze.description,
	...edit.description,
];
