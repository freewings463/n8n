"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v1/actions/text/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./classify.operation、./message.operation。导出:classify、message、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v1/actions/text/index.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/v1/actions/text/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as classify from './classify.operation';
import * as message from './message.operation';

export { classify, message };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Message a Model',
				value: 'message',
				action: 'Message a model',
				// eslint-disable-next-line n8n-nodes-base/node-param-description-excess-final-period
				description: 'Create a completion with GPT 3, 4, etc.',
			},
			{
				name: 'Classify Text for Violations',
				value: 'classify',
				action: 'Classify text for violations',
				description: 'Check whether content complies with usage policies',
			},
		],
		default: 'message',
		displayOptions: {
			show: {
				resource: ['text'],
			},
		},
	},

	...classify.description,
	...message.description,
];
