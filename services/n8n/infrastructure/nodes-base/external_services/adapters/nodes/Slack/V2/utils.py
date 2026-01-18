"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Slack/V2/utils.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Slack/V2 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:slackChannelModes。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。注释目标:eslint-disable n8n-nodes-base/node-param-default-missing。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Slack/V2/utils.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Slack/V2/utils.py

/* eslint-disable n8n-nodes-base/node-param-default-missing */
import type { INodePropertyMode } from 'n8n-workflow';

export const slackChannelModes: INodePropertyMode[] = [
	{
		displayName: 'From List',
		name: 'list',
		type: 'list',
		placeholder: 'Select a channel...',
		typeOptions: {
			searchListMethod: 'getChannels',
			searchable: true,
			slowLoadNotice: {
				message: 'If loading is slow, try selecting a channel using "By ID" or "By URL"',
				timeout: 15000,
			},
		},
	},
	{
		displayName: 'By ID',
		name: 'id',
		type: 'string',
		validation: [
			{
				type: 'regex',
				properties: {
					regex: '[a-zA-Z0-9]{2,}',
					errorMessage: 'Not a valid Slack Channel ID',
				},
			},
		],
		placeholder: 'C0122KQ70S7E',
	},
	{
		displayName: 'By URL',
		name: 'url',
		type: 'string',
		placeholder: 'https://app.slack.com/client/TS9594PZK/B0556F47Z3A',
		validation: [
			{
				type: 'regex',
				properties: {
					regex: 'http(s)?://app.slack.com/client/.*/([a-zA-Z0-9]{2,})',
					errorMessage: 'Not a valid Slack Channel URL',
				},
			},
		],
		extractValue: {
			type: 'regex',
			regex: 'https://app.slack.com/client/.*/([a-zA-Z0-9]{2,})',
		},
	},
];
