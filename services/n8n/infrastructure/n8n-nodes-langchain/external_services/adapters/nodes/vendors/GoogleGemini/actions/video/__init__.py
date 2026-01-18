"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/video/index.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini 的入口。导入/依赖:外部:无；内部:n8n-workflow；本地:./analyze.operation、./download.operation、./generate.operation。导出:analyze、download、generate、description。关键函数/方法:无。用于汇总导出并完成该模块模块初始化、注册或装配。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/video/index.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/GoogleGemini/actions/video/__init__.py

import type { INodeProperties } from 'n8n-workflow';

import * as analyze from './analyze.operation';
import * as download from './download.operation';
import * as generate from './generate.operation';

export { analyze, download, generate };

export const description: INodeProperties[] = [
	{
		displayName: 'Operation',
		name: 'operation',
		type: 'options',
		noDataExpression: true,
		options: [
			{
				name: 'Analyze Video',
				value: 'analyze',
				action: 'Analyze video',
				description: 'Take in videos and answer questions about them',
			},
			{
				name: 'Generate a Video',
				value: 'generate',
				action: 'Generate a video',
				description: 'Creates a video from a text prompt',
			},
			{
				name: 'Download Video',
				value: 'download',
				action: 'Download a video',
				description: 'Download a generated video from the Google Gemini API using a URL',
			},
		],
		default: 'generate',
		displayOptions: {
			show: {
				resource: ['video'],
			},
		},
	},
	...analyze.description,
	...download.description,
	...generate.description,
];
