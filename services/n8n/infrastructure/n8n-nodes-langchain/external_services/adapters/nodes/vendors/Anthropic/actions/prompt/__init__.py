"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/actions/prompt/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/Anthropic 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./generate.operation、./improve.operation、./templatize.operation。导出:generate、improve、templatize、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/actions/prompt/index.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/Anthropic/actions/prompt/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as generate from './generate.operation';
import * as improve from './improve.operation';
import * as templatize from './templatize.operation';

export { generate, improve, templatize };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Generate Prompt',
				value: 'generate',
				action: 'Generate a prompt',
				description: 'Generate a prompt for a model',
			},
			{
				name: 'Improve Prompt',
				value: 'improve',
				action: 'Improve a prompt',
				description: 'Improve a prompt for a model',
			},
			{
				name: 'Templatize Prompt',
				value: 'templatize',
				action: 'Templatize a prompt',
				description: 'Templatize a prompt for a model',
			},
		],
		default: 'generate',
		displayOptions: {
			show: {
				resource: ['prompt'],
			},
		},
	},
	{
		displayName:
			'The <a href="https://docs.anthropic.com/en/api/prompt-tools-generate">prompt tools APIs</a> are in a closed research preview. Your organization must request access to use them.',
		name: 'experimentalNotice',
		type: 'notice',
		default: '',
		displayOptions: {
			show: {
				resource: ['prompt'],
			},
		},
	},
	...generate.description,
	...improve.description,
	...templatize.description,
];
