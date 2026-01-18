"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Salesmate/DealInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Salesmate 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:IDeal。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Salesmate/DealInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Salesmate/DealInterface.py

export interface IDeal {
	title?: string;
	owner?: number;
	pipeline?: string;
	primaryContact?: number;
	primaryCompany?: number;
	status?: string;
	stage?: string;
	source?: string;
	estimatedCloseDate?: string;
	dealValue?: number;
	currency?: string;
	priority?: string;
	description?: string;
	tags?: string;
}
