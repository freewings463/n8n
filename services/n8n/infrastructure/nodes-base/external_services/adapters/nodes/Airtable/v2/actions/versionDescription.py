"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Airtable/v2/actions/versionDescription.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Airtable/v2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./base/Base.resource、./record/Record.resource。导出:versionDescription。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-filename-against-convention。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Airtable/v2/actions/versionDescription.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Airtable/v2/actions/versionDescription.py

/* eslint-disable n8n-nodes-base/node-filename-against-convention */
import { NodeConnectionTypes, type INodeTypeDescription } from 'n8n-workflow';

import * as base from './base/Base.resource';
import * as record from './record/Record.resource';

export const versionDescription: INodeTypeDescription = {
	displayName: 'Airtable',
	name: 'airtable',
	icon: 'file:airtable.svg',
	group: ['input'],
	version: [2, 2.1],
	subtitle: '={{ $parameter["operation"] + ": " + $parameter["resource"] }}',
	description: 'Read, update, write and delete data from Airtable',
	defaults: {
		name: 'Airtable',
	},
	inputs: [NodeConnectionTypes.Main],
	outputs: [NodeConnectionTypes.Main],
	credentials: [
		{
			name: 'airtableTokenApi',
			required: true,
			displayOptions: {
				show: {
					authentication: ['airtableTokenApi'],
				},
			},
		},
		{
			name: 'airtableOAuth2Api',
			required: true,
			displayOptions: {
				show: {
					authentication: ['airtableOAuth2Api'],
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
					name: 'Access Token',
					value: 'airtableTokenApi',
				},
				{
					name: 'OAuth2',
					value: 'airtableOAuth2Api',
				},
			],
			default: 'airtableTokenApi',
		},
		{
			displayName: 'Resource',
			name: 'resource',
			type: 'options',
			noDataExpression: true,
			options: [
				{
					name: 'Base',
					value: 'base',
				},
				{
					name: 'Record',
					value: 'record',
				},
				// {
				// 	name: 'Table',
				// 	value: 'table',
				// },
			],
			default: 'record',
		},
		...record.description,
		...base.description,
	],
};
