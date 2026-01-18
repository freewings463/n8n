"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V2/description.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:@utils/sharedFields；内部:n8n-workflow；本地:../options。导出:getToolsAgentProperties。关键函数/方法:getToolsAgentProperties、getBatchingOptionFields。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/V2/description.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/agents/ToolsAgent/V2/description.py

import type { INodeProperties } from 'n8n-workflow';

import { getBatchingOptionFields } from '@utils/sharedFields';

import { commonOptions } from '../options';

const enableStreaminOption: INodeProperties = {
	displayName: 'Enable Streaming',
	name: 'enableStreaming',
	type: 'boolean',
	default: true,
	description: 'Whether this agent will stream the response in real-time as it generates text',
};

export const getToolsAgentProperties = ({
	withStreaming,
}: { withStreaming: boolean }): INodeProperties[] => [
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		default: {},
		placeholder: 'Add Option',
		options: [
			...commonOptions,
			getBatchingOptionFields(undefined, 1),
			...(withStreaming ? [enableStreaminOption] : []),
		],
		displayOptions: {
			hide: {
				'@version': [{ _cnd: { lt: 2.2 } }],
			},
		},
	},
	{
		displayName: 'Options',
		name: 'options',
		type: 'collection',
		default: {},
		placeholder: 'Add Option',
		options: [...commonOptions, getBatchingOptionFields(undefined, 1)],
		displayOptions: {
			show: {
				'@version': [{ _cnd: { lt: 2.2 } }],
			},
		},
	},
];
