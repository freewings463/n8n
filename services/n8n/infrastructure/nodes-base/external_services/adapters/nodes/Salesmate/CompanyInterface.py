"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Salesmate/CompanyInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Salesmate 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:ICompany。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Salesmate/CompanyInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Salesmate/CompanyInterface.py

export interface ICompany {
	name?: string;
	owner?: number;
	website?: string;
	phone?: string;
	otherPhone?: string;
	googlePlusHandle?: string;
	linkedInHandle?: string;
	facebookHandle?: string;
	linkedinHandle?: string;
	skypeId?: string;
	twitterHandle?: string;
	currency?: string;
	billingAddressLine1?: string;
	billingAddressLine2?: string;
	billingCity?: string;
	billingZipCode?: string;
	billingCountry?: string;
	billingState?: string;
	description?: string;
	tags?: string;
}
