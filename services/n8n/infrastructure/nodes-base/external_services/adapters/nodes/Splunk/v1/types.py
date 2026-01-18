"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Splunk/v1/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Splunk/v1 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:SplunkCredentials、SplunkFeedResponse、SplunkSearchResponse、SplunkResultResponse、SplunkError、SPLUNK。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Splunk/v1/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Splunk/v1/types.py

export type SplunkCredentials = {
	authToken: string;
	baseUrl: string;
	allowUnauthorizedCerts: boolean;
};

export type SplunkFeedResponse = {
	feed: {
		entry: { title: string };
	};
};

export type SplunkSearchResponse = {
	entry: { title: string };
};

export type SplunkResultResponse = {
	results: { result: Array<{ field: string }> } | { result: { field: string } };
};

export type SplunkError = {
	response?: {
		messages?: {
			msg: {
				$: { type: string };
				_: string;
			};
		};
	};
};

export const SPLUNK = {
	DICT: 's:dict',
	LIST: 's:list',
	ITEM: 's:item',
	KEY: 's:key',
};
