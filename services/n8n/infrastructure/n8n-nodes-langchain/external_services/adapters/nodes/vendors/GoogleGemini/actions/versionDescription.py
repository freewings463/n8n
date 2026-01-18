"""
MIGRATION-META:
  source_path: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/versionDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./audio、./document、./file、./fileSearch 等3项。导出:versionDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-filename-against-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/@n8n/nodes-langchain/nodes/vendors/GoogleGemini/actions/versionDescription.ts -> services/n8n/infrastructure/n8n-nodes-langchain/external_services/adapters/nodes/vendors/GoogleGemini/actions/versionDescription.py

/* eslint-disable n8n-nodes-base/node-filename-against-convention */
import { NodeConnectionTypes, type INodeTypeDescription } from 'n8n-workflow';

import * as audio from './audio';
import * as document from './document';
import * as file from './file';
import * as fileSearch from './fileSearch';
import * as image from './image';
import * as text from './text';
import * as video from './video';

export const versionDescription: INodeTypeDescription = {
	displayName: 'Google Gemini',
	name: 'googleGemini',
	icon: 'file:gemini.svg',
	group: ['transform'],
	version: [1, 1.1],
	defaultVersion: 1.1,
	subtitle: '={{ $parameter["operation"] + ": " + $parameter["resource"] }}',
	description: 'Interact with Google Gemini AI models',
	defaults: {
		name: 'Google Gemini',
	},
	usableAsTool: true,
	codex: {
		alias: ['LangChain', 'video', 'document', 'audio', 'transcribe', 'assistant'],
		categories: ['AI'],
		subcategories: {
			AI: ['Agents', 'Miscellaneous', 'Root Nodes'],
		},
		resources: {
			primaryDocumentation: [
				{
					url: 'https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-langchain.googlegemini/',
				},
			],
		},
	},
	inputs: `={{
		(() => {
			const resource = $parameter.resource;
	  	const operation = $parameter.operation;
			if (resource === 'text' && operation === 'message') {
				return [{ type: 'main' }, { type: 'ai_tool', displayName: 'Tools' }];
			}

			return ['main'];
		})()
	}}`,
	outputs: [NodeConnectionTypes.Main],
	credentials: [
		{
			name: 'googlePalmApi',
			required: true,
		},
	],
	properties: [
		{
			displayName: 'Resource',
			name: 'resource',
			type: 'options',
			noDataExpression: true,
			options: [
				{
					name: 'Audio',
					value: 'audio',
				},
				{
					name: 'Document',
					value: 'document',
				},
				{
					name: 'File Search',
					value: 'fileSearch',
				},
				{
					name: 'Image',
					value: 'image',
				},
				{
					name: 'Media File',
					value: 'file',
				},
				{
					name: 'Text',
					value: 'text',
				},
				{
					name: 'Video',
					value: 'video',
				},
			],
			default: 'text',
		},
		...audio.description,
		...document.description,
		...file.description,
		...fileSearch.description,
		...image.description,
		...text.description,
		...video.description,
	],
};
