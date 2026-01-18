"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Elastic/Elasticsearch/types.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Elastic/Elasticsearch 的类型。导入/依赖:外部:无；内部:无；本地:无。导出:ElasticsearchApiCredentials、DocumentGetAllOptions、FieldsUiValues。关键函数/方法:无。用于定义该模块相关类型/结构约束，供多模块共享。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Elastic/Elasticsearch/types.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Elastic/Elasticsearch/types.py

export type ElasticsearchApiCredentials = {
	username: string;
	password: string;
	baseUrl: string;
	ignoreSSLIssues: boolean;
};

export type DocumentGetAllOptions = Partial<{
	allow_no_indices: boolean;
	allow_partial_search_results: boolean;
	batched_reduce_size: number;
	ccs_minimize_roundtrips: boolean;
	docvalue_fields: string;
	expand_wildcards: 'All' | 'Closed' | 'Hidden' | 'None' | 'Open';
	explain: boolean;
	ignore_throttled: boolean;
	ignore_unavailable: boolean;
	max_concurrent_shard_requests: number;
	pre_filter_shard_size: number;
	query: string;
	request_cache: boolean;
	routing: string;
	search_type: 'query_then_fetch' | 'dfs_query_then_fetch';
	seq_no_primary_term: boolean;
	sort: string;
	_source: boolean;
	_source_excludes: string;
	_source_includes: string;
	stats: string;
	stored_fields: boolean;
	terminate_after: boolean;
	timeout: number;
	track_scores: boolean;
	track_total_hits: string;
	version: boolean;
}>;

export type FieldsUiValues = Array<{
	fieldId: string;
	fieldValue: string;
}>;
