"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v2/actions/text/classify.operation.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../../transport。导出:description。关键函数/方法:execute。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v2/actions/text/classify.operation.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/v2/actions/text/classify_operation.py

import type { INodeProperties, IExecuteFunctions, INodeExecutionData } from 'n8n-workflow';
import { updateDisplayOptions } from 'n8n-workflow';

import { apiRequest } from '../../../transport';

const properties: INodeProperties[] = [
	{
		displayName: 'Text Input',
		name: 'input',
		type: 'string',
		placeholder: 'e.g. Sample text goes here',
		description: 'The input text to classify if it is violates the moderation policy',
		default: '',
		typeOptions: {
			rows: 2,
		},
	},
	{
		displayName: 'Simplify Output',
		name: 'simplify',
		type: 'boolean',
		default: false,
		description: 'Whether to return a simplified version of the response instead of the raw data',
	},
	{
		displayName: 'Options',
		name: 'options',
		placeholder: 'Add Option',
		type: 'collection',
		default: {},
		options: [
			{
				displayName: 'Use Stable Model',
				name: 'useStableModel',
				type: 'boolean',
				default: false,
				description:
					'Whether to use the stable version of the model instead of the latest version, accuracy may be slightly lower',
			},
		],
		displayOptions: {
			show: {
				'@version': [{ _cnd: { lt: 2.1 } }],
			},
		},
	},
];

const displayOptions = {
	show: {
		operation: ['classify'],
		resource: ['text'],
	},
};

export const description = updateDisplayOptions(displayOptions, properties);

export async function execute(this: IExecuteFunctions, i: number): Promise<INodeExecutionData[]> {
	const input = this.getNodeParameter('input', i) as string;
	const version = this.getNode().typeVersion;
	let model = 'omni-moderation-latest';
	if (version < 2.1) {
		const options = this.getNodeParameter('options', i);
		model = options.useStableModel ? 'text-moderation-stable' : 'text-moderation-latest';
	}

	const body = {
		input,
		model,
	};

	const { results } = await apiRequest.call(this, 'POST', '/moderations', { body });

	if (!results) return [];

	const simplify = this.getNodeParameter('simplify', i) as boolean;

	if (simplify && results) {
		return [
			{
				json: { flagged: results[0].flagged },
				pairedItem: { item: i },
			},
		];
	} else {
		return [
			{
				json: results[0],
				pairedItem: { item: i },
			},
		];
	}
}
