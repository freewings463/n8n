"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v1/actions/audio/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/OpenAi 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./generate.operation、./transcribe.operation、./translate.operation。导出:generate、transcribe、translate、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/OpenAi/v1/actions/audio/index.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/OpenAi/v1/actions/audio/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as generate from './generate.operation';
import * as transcribe from './transcribe.operation';
import * as translate from './translate.operation';

export { generate, transcribe, translate };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Generate Audio',
				value: 'generate',
				action: 'Generate audio',
				description: 'Creates audio from a text prompt',
			},
			{
				name: 'Transcribe a Recording',
				value: 'transcribe',
				action: 'Transcribe a recording',
				description: 'Transcribes audio into text',
			},
			{
				name: 'Translate a Recording',
				value: 'translate',
				action: 'Translate a recording',
				description: 'Translates audio into text in English',
			},
		],
		default: 'generate',
		displayOptions: {
			show: {
				resource: ['audio'],
			},
		},
	},
	{
		displayName: 'OpenAI API limits the size of the audio file to 25 MB',
		name: 'fileSizeLimitNotice',
		type: 'notice',
		default: ' ',
		displayOptions: {
			show: {
				resource: ['audio'],
				operation: ['translate', 'transcribe'],
			},
		},
	},
	...generate.description,
	...transcribe.description,
	...translate.description,
];
