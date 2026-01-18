"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Xero/IContactInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Xero 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:IAddress、IPhone、IContact、ITenantId。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Xero/IContactInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Xero/IContactInterface.py

export interface IAddress {
	AddressType?: string;
	AddressLine1?: string;
	AddressLine2?: string;
	City?: string;
	Region?: string;
	PostalCode?: string;
	Country?: string;
	AttentionTo?: string;
}

export interface IPhone {
	PhoneType?: string;
	PhoneNumber?: string;
	PhoneAreaCode?: string;
	PhoneCountryCode?: string;
}

export interface IContact extends ITenantId {
	AccountNumber?: string;
	Addresses?: IAddress[];
	BankAccountDetails?: string;
	ContactId?: string;
	ContactNumber?: string;
	ContactStatus?: string;
	DefaultCurrency?: string;
	EmailAddress?: string;
	FirstName?: string;
	LastName?: string;
	Name?: string;
	Phones?: IPhone[];
	PurchaseTrackingCategory?: string;
	PurchasesDefaultAccountCode?: string;
	SalesDefaultAccountCode?: string;
	SalesTrackingCategory?: string;
	SkypeUserName?: string;
	taxNumber?: string;
	xeroNetworkKey?: string;
}

export interface ITenantId {
	organizationId?: string;
}
