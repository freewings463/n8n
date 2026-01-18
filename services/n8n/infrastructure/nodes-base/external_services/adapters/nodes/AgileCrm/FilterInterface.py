"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/AgileCrm/FilterInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/AgileCrm 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:ISearchConditions、IFilterRules、IFilter。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/AgileCrm/FilterInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/AgileCrm/FilterInterface.py

export interface ISearchConditions {
	field?: string;
	condition_type?: string;
	value?: string;
	value2?: string;
}

export interface IFilterRules {
	LHS?: string;
	CONDITION?: string;
	RHS?: string;
	RHS_NEW?: string;
}

export interface IFilter {
	or_rules?: IFilterRules;
	rules?: IFilterRules;
	contact_type?: string;
}
