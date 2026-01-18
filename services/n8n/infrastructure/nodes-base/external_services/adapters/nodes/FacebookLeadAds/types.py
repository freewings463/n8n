"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/FacebookLeadAds/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/FacebookLeadAds 的类型。导入/依赖:外部:无；内部:n8n-workflow；本地:无。导出:BaseFacebookResponse、BasePaginatedFacebookResponse、FacebookAppWebhookSubscriptionsResponse、FacebookAppWebhookSubscription、FacebookAppWebhookSubscriptionField、CreateFacebookAppWebhookSubscription、FacebookPageListResponse、FacebookFormListResponse 等7项。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/FacebookLeadAds/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/FacebookLeadAds/types.py

import type { GenericValue } from 'n8n-workflow';

export type BaseFacebookResponse<TData> = { data: TData };
export type BasePaginatedFacebookResponse<TData> = BaseFacebookResponse<TData> & {
	paging: { cursors: { before?: string; after?: string }; next?: string };
};

export type FacebookAppWebhookSubscriptionsResponse = BaseFacebookResponse<
	FacebookAppWebhookSubscription[]
>;

export interface FacebookAppWebhookSubscription {
	object: string;
	callback_url: string;
	active: boolean;
	fields: FacebookAppWebhookSubscriptionField[];
}

export interface FacebookAppWebhookSubscriptionField {
	name: string;
	version: string;
}

export interface CreateFacebookAppWebhookSubscription {
	object: string;
	callback_url: string;
	fields: string[];
	include_values: boolean;
	verify_token: string;
}

export type FacebookPageListResponse = BasePaginatedFacebookResponse<FacebookPage[]>;
export type FacebookFormListResponse = BasePaginatedFacebookResponse<FacebookForm[]>;

export interface FacebookPage {
	id: string;
	name: string;
	access_token: string;
	category: string;
	category_list: FacebookPageCategory[];
	tasks: string[];
}

export interface FacebookPageCategory {
	id: string;
	name: string;
}

export interface FacebookFormQuestion {
	id: string;
	key: string;
	label: string;
	type: string;
}

export interface FacebookForm {
	id: string;
	name: string;
	locale: string;
	status: string;
	page: {
		id: string;
		name: string;
	};
	questions: FacebookFormQuestion[];
}

export interface FacebookPageEvent {
	object: 'page';
	entry: FacebookPageEventEntry[];
}

export interface FacebookPageEventEntry {
	id: string;
	time: number;
	changes: [
		{
			field: 'leadgen';
			value: {
				ad_id: string;
				form_id: string;
				leadgen_id: string;
				created_time: number;
				page_id: string;
				adgroup_id: string;
			};
		},
	];
}

export interface FacebookFormLeadData {
	id: string;
	created_time: string;
	ad_id: string;
	ad_name: string;
	adset_id: string;
	adset_name: string;
	form_id: string;
	field_data: [
		{
			name: string;
			values: GenericValue[];
		},
	];
}
