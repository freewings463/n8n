"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/actions/descriptions.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/Anthropic 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:modelRLC。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/Anthropic/actions/descriptions.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/Anthropic/actions/descriptions.py

import type { INodeProperties } from 'n8n-workflow';

export const modelRLC: INodeProperties = {
	displayName: 'Model',
	name: 'modelId',
	type: 'resourceLocator',
	default: { mode: 'list', value: '' },
	required: true,
	modes: [
		{
			displayName: 'From List',
			name: 'list',
			type: 'list',
			typeOptions: {
				searchListMethod: 'modelSearch',
				searchable: true,
			},
		},
		{
			displayName: 'ID',
			name: 'id',
			type: 'string',
			placeholder: 'e.g. claude-sonnet-4-5-20250929',
		},
	],
};
