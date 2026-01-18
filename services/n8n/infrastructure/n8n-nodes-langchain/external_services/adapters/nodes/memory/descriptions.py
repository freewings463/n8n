"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/memory/descriptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/memory 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:sessionIdOption、expressionSessionKeyProperty、sessionKeyProperty、contextWindowLengthProperty。关键函数/方法:expressionSessionKeyProperty。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/memory/descriptions.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/memory/descriptions.py

import type { INodeProperties } from 'n8n-workflow';

export const sessionIdOption: INodeProperties = {
	displayName: 'Session ID',
	name: 'sessionIdType',
	type: 'options',
	options: [
		{
			name: 'Connected Chat Trigger Node',
			value: 'fromInput',
			description:
				"Looks for an input field called 'sessionId' that is coming from a directly connected Chat Trigger",
		},
		{
			// eslint-disable-next-line n8n-nodes-base/node-param-display-name-miscased
			name: 'Define below',
			value: 'customKey',
			description: 'Use an expression to reference data in previous nodes or enter static text',
		},
	],
	default: 'fromInput',
};

export const expressionSessionKeyProperty = (fromVersion: number): INodeProperties => ({
	displayName: 'Session Key From Previous Node',
	name: 'sessionKey',
	type: 'string',
	default: '={{ $json.sessionId }}',
	disabledOptions: { show: { sessionIdType: ['fromInput'] } },
	displayOptions: {
		show: {
			sessionIdType: ['fromInput'],
			'@version': [{ _cnd: { gte: fromVersion } }],
		},
	},
});

export const sessionKeyProperty: INodeProperties = {
	displayName: 'Key',
	name: 'sessionKey',
	type: 'string',
	default: '',
	description: 'The key to use to store session ID in the memory',
	displayOptions: {
		show: {
			sessionIdType: ['customKey'],
		},
	},
};

export const contextWindowLengthProperty: INodeProperties = {
	displayName: 'Context Window Length',
	name: 'contextWindowLength',
	type: 'number',
	default: 5,
	hint: 'How many past interactions the model receives as context',
};
