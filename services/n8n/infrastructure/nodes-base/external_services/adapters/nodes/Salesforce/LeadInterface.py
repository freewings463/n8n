"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Salesforce/LeadInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Salesforce 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:ILead。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Salesforce/LeadInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Salesforce/LeadInterface.py

export interface ILead {
	[key: string]: any;
	Company?: string;
	LastName?: string;
	Email?: string;
	Fax?: number;
	City?: string;
	Phone?: string;
	State?: string;
	Title?: string;
	Jigsaw?: string;
	Rating?: string;
	Status?: string;
	Street?: string;
	Country?: string;
	OwnerId?: string;
	Website?: string;
	Industry?: string;
	FirstName?: string;
	LeadSource?: string;
	PostalCode?: string;
	Salutation?: string;
	Description?: string;
	AnnualRevenue?: number;
	IsUnreadByOwner?: boolean;
	NumberOfEmployees?: number;
	MobilePhone?: string;
	HasOptedOutOfEmail?: boolean;
	HasOptedOutOfFax?: boolean;
}
