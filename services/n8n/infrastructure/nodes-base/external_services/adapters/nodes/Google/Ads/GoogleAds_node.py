"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/Ads/GoogleAds.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/Ads 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./CampaignDescription。导出:GoogleAds。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/Ads/GoogleAds.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/Ads/GoogleAds_node.py

import { NodeConnectionTypes, type INodeType, type INodeTypeDescription } from 'n8n-workflow';

import { campaignFields, campaignOperations } from './CampaignDescription';

export class GoogleAds implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Google Ads',
		name: 'googleAds',
		icon: 'file:googleAds.svg',
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Use the Google Ads API',
		defaults: {
			name: 'Google Ads',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		credentials: [
			{
				name: 'googleAdsOAuth2Api',
				required: true,
				testedBy: {
					request: {
						method: 'GET',
						url: '/v20/customers:listAccessibleCustomers',
					},
				},
			},
		],
		requestDefaults: {
			returnFullResponse: true,
			baseURL: 'https://googleads.googleapis.com',
			headers: {
				'developer-token': '={{$credentials.developerToken}}',
			},
		},
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Campaign',
						value: 'campaign',
					},
				],
				default: 'campaign',
			},
			//-------------------------------
			// Campaign Operations
			//-------------------------------
			...campaignOperations,
			{
				displayName:
					'Divide field names expressed with <i>micros</i> by 1,000,000 to get the actual value',
				name: 'campaigsNotice',
				type: 'notice',
				default: '',
				displayOptions: {
					show: {
						resource: ['campaign'],
					},
				},
			},
			...campaignFields,
		],
	};
}
