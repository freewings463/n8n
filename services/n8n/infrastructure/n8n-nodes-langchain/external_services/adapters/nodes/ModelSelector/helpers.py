"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/ModelSelector/helpers.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/ModelSelector 的工具。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:numberInputsProperty、configuredInputs。关键函数/方法:configuredInputs。用于提供该模块通用工具能力（纯函数/封装器）供复用。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/ModelSelector/helpers.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/ModelSelector/helpers.py

import type { INodeInputConfiguration, INodeParameters, INodeProperties } from 'n8n-workflow';

export const numberInputsProperty: INodeProperties = {
	displayName: 'Number of Inputs',
	name: 'numberInputs',
	type: 'options',
	noDataExpression: true,
	default: 2,
	options: [
		{
			name: '2',
			value: 2,
		},
		{
			name: '3',
			value: 3,
		},
		{
			name: '4',
			value: 4,
		},
		{
			name: '5',
			value: 5,
		},
		{
			name: '6',
			value: 6,
		},
		{
			name: '7',
			value: 7,
		},
		{
			name: '8',
			value: 8,
		},
		{
			name: '9',
			value: 9,
		},
		{
			name: '10',
			value: 10,
		},
	],
	validateType: 'number',
	description:
		'The number of data inputs you want to merge. The node waits for all connected inputs to be executed.',
};

export function configuredInputs(parameters: INodeParameters): INodeInputConfiguration[] {
	return Array.from({ length: (parameters.numberInputs as number) || 2 }, (_, i) => ({
		type: 'ai_languageModel',
		displayName: `Model ${(i + 1).toString()}`,
		required: true,
		maxConnections: 1,
	}));
}
