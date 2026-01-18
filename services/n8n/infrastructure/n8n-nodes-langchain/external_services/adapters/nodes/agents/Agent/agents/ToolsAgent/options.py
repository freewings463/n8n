"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/options.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/agents/Agent 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./prompt。导出:commonOptions。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/ToolsAgent/options.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/agents/Agent/agents/ToolsAgent/options.py

import type { INodeProperties } from 'n8n-workflow';

import { SYSTEM_MESSAGE } from './prompt';

export const commonOptions: INodeProperties[] = [
	{
		displayName: 'System Message',
		name: 'systemMessage',
		type: 'string',
		default: SYSTEM_MESSAGE,
		description: 'The message that will be sent to the agent before the conversation starts',
		typeOptions: {
			rows: 6,
		},
	},
	{
		displayName: 'Max Iterations',
		name: 'maxIterations',
		type: 'number',
		default: 10,
		description: 'The maximum number of iterations the agent will run before stopping',
	},
	{
		displayName: 'Return Intermediate Steps',
		name: 'returnIntermediateSteps',
		type: 'boolean',
		default: false,
		description: 'Whether or not the output should include intermediate steps the agent took',
	},
	{
		displayName: 'Automatically Passthrough Binary Images',
		name: 'passthroughBinaryImages',
		type: 'boolean',
		default: true,
		description:
			'Whether or not binary images should be automatically passed through to the agent as image type messages',
	},
];
