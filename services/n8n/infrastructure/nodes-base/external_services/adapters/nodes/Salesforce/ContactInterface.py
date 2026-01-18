"""
MIGRATION-META:
  source_path: packages/nodes-base/nodes/Salesforce/ContactInterface.ts
  target_context: n8n
  target_layer: Infrastructure
  responsibility: 位于 packages/nodes-base/nodes/Salesforce 的节点。导入/依赖:外部:无；内部:无；本地:无。导出:IContact。关键函数/方法:无。用于实现 n8n 该模块节点的描述与执行逻辑，供工作流运行。
  entities: []
  external_dependencies: []
  mapping_confidence: High
  todo_refactor_ddd:
    - Node integration -> external_services adapters (ACL)
    - Rewrite implementation for Infrastructure layer
  moved_in_batch: 2026-01-18-system-analysis-ddd-mapping
"""
# TODO-REFACTOR-DDD: packages/nodes-base/nodes/Salesforce/ContactInterface.ts -> services/n8n/infrastructure/nodes-base/external_services/adapters/nodes/Salesforce/ContactInterface.py

export interface IContact {
	[key: string]: any;
	LastName?: string;
	Fax?: string;
	Email?: string;
	Phone?: string;
	Title?: string;
	Jigsaw?: string;
	OwnerId?: string;
	AccountId?: string;
	Birthdate?: string;
	FirstName?: string;
	HomePhone?: string;
	OtherCity?: string;
	Department?: string;
	LeadSource?: string;
	OtherPhone?: string;
	OtherState?: string;
	Salutation?: string;
	Description?: string;
	MailingCity?: string;
	MobilePhone?: string;
	OtherStreet?: string;
	MailingState?: string;
	OtherCountry?: string;
	AssistantName?: string;
	MailingStreet?: string;
	AssistantPhone?: string;
	MailingCountry?: string;
	OtherPostalCode?: string;
	MailingPostalCode?: string;
	EmailBouncedDate?: string;
	EmailBouncedReason?: string;
}
