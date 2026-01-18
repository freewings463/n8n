"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Notion/v1/VersionDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Notion/v1 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:../descriptions/BlockDescription、../descriptions/DatabaseDescription、../descriptions/PageDescription、../descriptions/UserDescription。导出:versionDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-filename-against-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Notion/v1/VersionDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Notion/v1/VersionDescription.py

/* eslint-disable n8n-nodes-base/node-filename-against-convention */
import { NodeConnectionTypes, type INodeTypeDescription } from 'n8n-workflow';

import { blockFields, blockOperations } from '../shared/descriptions/BlockDescription';
import { databaseFields, databaseOperations } from '../shared/descriptions/DatabaseDescription';
import {
	databasePageFields,
	databasePageOperations,
} from '../shared/descriptions/DatabasePageDescription';
import { pageFields, pageOperations } from '../shared/descriptions/PageDescription';
import { userFields, userOperations } from '../shared/descriptions/UserDescription';

export const versionDescription: INodeTypeDescription = {
	displayName: 'Notion',
	name: 'notion',
	icon: 'file:notion.svg',
	group: ['output'],
	version: 1,
	subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
	description: 'Consume Notion API',
	defaults: {
		name: 'Notion',
	},
	inputs: [NodeConnectionTypes.Main],
	outputs: [NodeConnectionTypes.Main],
	credentials: [
		{
			name: 'notionApi',
			required: true,
			// displayOptions: {
			// 	show: {
			// 		authentication: [
			// 			'apiKey',
			// 		],
			// 	},
			// },
		},
		// {
		// 	name: 'notionOAuth2Api',
		// 	required: true,
		// 	displayOptions: {
		// 		show: {
		// 			authentication: [
		// 				'oAuth2',
		// 			],
		// 		},
		// 	},
		// },
	],
	properties: [
		// {
		// 	displayName: 'Authentication',
		// 	name: 'authentication',
		// 	type: 'options',
		// 	options: [
		// 		{
		// 			name: 'API Key',
		// 			value: 'apiKey',
		// 		},
		// 		{
		// 			name: 'OAuth2',
		// 			value: 'oAuth2',
		// 		},
		// 	],
		// 	default: 'apiKey',
		// 	description: 'The resource to operate on.',
		// },
		{
			displayName:
				'In Notion, make sure to <a href="https://www.notion.so/help/add-and-manage-connections-with-the-api" target="_blank">add your connection</a> to the pages you want to access.',
			name: 'notionNotice',
			type: 'notice',
			default: '',
		},
		{
			displayName: 'Resource',
			name: 'resource',
			type: 'options',
			noDataExpression: true,
			options: [
				{
					name: 'Block',
					value: 'block',
				},
				{
					name: 'Database',
					value: 'database',
				},
				{
					name: 'Database Page',
					value: 'databasePage',
				},
				{
					name: 'Page',
					value: 'page',
				},
				{
					name: 'User',
					value: 'user',
				},
			],
			default: 'page',
		},
		...blockOperations,
		...blockFields,
		...databaseOperations,
		...databaseFields,
		...databasePageOperations,
		...databasePageFields,
		...pageOperations,
		...pageFields,
		...userOperations,
		...userFields,
	],
};
