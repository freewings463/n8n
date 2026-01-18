"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Google/BusinessProfile/GoogleBusinessProfile.node.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Google/BusinessProfile 的节点。导入/依赖:外部:无；内部:n8n-workflow；本地:./GenericFunctions、./PostDescription、./ReviewDescription。导出:GoogleBusinessProfile。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Detected INodeType adapter
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Google/BusinessProfile/GoogleBusinessProfile.node.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Google/BusinessProfile/GoogleBusinessProfile_node.py

import { NodeConnectionTypes, type INodeType, type INodeTypeDescription } from 'n8n-workflow';

import { searchAccounts, searchLocations, searchPosts, searchReviews } from './GenericFunctions';
import { postFields, postOperations } from './PostDescription';
import { reviewFields, reviewOperations } from './ReviewDescription';

export class GoogleBusinessProfile implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Google Business Profile',
		name: 'googleBusinessProfile',
		icon: 'file:googleBusinessProfile.svg',
		group: ['input'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Consume Google Business Profile API',
		defaults: {
			name: 'Google Business Profile',
		},
		usableAsTool: true,
		inputs: [NodeConnectionTypes.Main],
		outputs: [NodeConnectionTypes.Main],
		hints: [
			{
				message: 'Please select a parameter in the options to modify the post',
				displayCondition:
					'={{$parameter["resource"] === "post" && $parameter["operation"] === "update" && Object.keys($parameter["additionalOptions"]).length === 0}}',
				whenToDisplay: 'always',
				location: 'outputPane',
				type: 'warning',
			},
		],
		credentials: [
			{
				name: 'googleBusinessProfileOAuth2Api',
				required: true,
			},
		],
		requestDefaults: {
			baseURL: 'https://mybusiness.googleapis.com/v4',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
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
						name: 'Post',
						value: 'post',
					},
					{
						name: 'Review',
						value: 'review',
					},
				],
				default: 'post',
			},
			...postOperations,
			...postFields,
			...reviewOperations,
			...reviewFields,
		],
	};

	methods = {
		listSearch: {
			searchAccounts,
			searchLocations,
			searchReviews,
			searchPosts,
		},
	};
}
