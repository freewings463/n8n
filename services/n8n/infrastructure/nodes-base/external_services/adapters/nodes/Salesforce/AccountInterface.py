"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Salesforce/AccountInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Salesforce 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:IAccount。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Salesforce/AccountInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Salesforce/AccountInterface.py

export interface IAccount {
	[key: string]: any;
	Name?: string;
	Fax?: string;
	Type?: string;
	Phone?: string;
	Jigsaw?: string;
	OwnerId?: string;
	SicDesc?: string;
	Website?: string;
	Industry?: string;
	ParentId?: string;
	BillingCity?: string;
	Description?: string;
	BillingState?: string;
	ShippingStreet?: string;
	ShippingCity?: string;
	AccountNumber?: string;
	AccountSource?: string;
	AnnualRevenue?: number;
	BillingStreet?: string;
	ShippingState?: string;
	BillingCountry?: string;
	ShippingCountry?: string;
	BillingPostalCode?: string;
	NumberOfEmployees?: string;
	ShippingPostalCode?: string;
}
