"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Microsoft/AzureCosmosDb/helpers/constants.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Microsoft/AzureCosmosDb 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:RESOURCE_TYPES、CURRENT_VERSION、HeaderConstants。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Microsoft/AzureCosmosDb/helpers/constants.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Microsoft/AzureCosmosDb/helpers/constants.py

export const RESOURCE_TYPES = [
	'dbs',
	'colls',
	'sprocs',
	'udfs',
	'triggers',
	'users',
	'permissions',
	'docs',
];

export const CURRENT_VERSION = '2018-12-31';

export const HeaderConstants = {
	AUTHORIZATION: 'authorization',
	X_MS_CONTINUATION: 'x-ms-continuation',
	X_MS_COSMOS_OFFER_AUTOPILOT_SETTING: 'x-ms-cosmos-offer-autopilot-setting',
	X_MS_DOCUMENTDB_IS_UPSERT: 'x-ms-documentdb-is-upsert',
	X_MS_DOCUMENTDB_PARTITIONKEY: 'x-ms-documentdb-partitionkey',
	X_MS_MAX_ITEM_COUNT: 'x-ms-max-item-count',
	X_MS_OFFER_THROUGHPUT: 'x-ms-offer-throughput',
};
