"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Drive/v2/actions/versionDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Drive 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./drive/Drive.resource、./file/File.resource、./fileFolder/FileFolder.resource、./folder/Folder.resource。导出:versionDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-filename-against-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Drive/v2/actions/versionDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Drive/v2/actions/versionDescription.py

/* eslint-disable n8n-nodes-base/node-filename-against-convention */
import { NodeConnectionTypes, type INodeTypeDescription } from 'n8n-workflow';

import * as drive from './drive/Drive.resource';
import * as file from './file/File.resource';
import * as fileFolder from './fileFolder/FileFolder.resource';
import * as folder from './folder/Folder.resource';

export const versionDescription: INodeTypeDescription = {
	displayName: 'Google Drive',
	name: 'googleDrive',
	icon: 'file:googleDrive.svg',
	group: ['input'],
	version: 3,
	subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
	description: 'Access data on Google Drive',
	defaults: {
		name: 'Google Drive',
	},
	inputs: [NodeConnectionTypes.Main],
	outputs: [NodeConnectionTypes.Main],
	usableAsTool: true,
	credentials: [
		{
			name: 'googleApi',
			required: true,
			displayOptions: {
				show: {
					authentication: ['serviceAccount'],
				},
			},
		},
		{
			name: 'googleDriveOAuth2Api',
			required: true,
			displayOptions: {
				show: {
					authentication: ['oAuth2'],
				},
			},
		},
	],
	properties: [
		{
			displayName: 'Authentication',
			name: 'authentication',
			type: 'options',
			options: [
				{
					// eslint-disable-next-line n8n-nodes-base/node-param-display-name-miscased
					name: 'OAuth2 (recommended)',
					value: 'oAuth2',
				},
				{
					name: 'Service Account',
					value: 'serviceAccount',
				},
			],
			default: 'oAuth2',
		},
		{
			displayName: 'Resource',
			name: 'resource',
			type: 'options',
			noDataExpression: true,
			options: [
				{
					name: 'File',
					value: 'file',
				},
				{
					name: 'File/Folder',
					value: 'fileFolder',
				},
				{
					name: 'Folder',
					value: 'folder',
				},
				{
					name: 'Shared Drive',
					value: 'drive',
				},
			],
			default: 'file',
		},
		...drive.description,
		...file.description,
		...fileFolder.description,
		...folder.description,
	],
};
